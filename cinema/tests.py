"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from urllib import urlencode
from django.test import TestCase
from django.core.urlresolvers import reverse

from models import Movie

USER_PASSWORDS = { # for movies.yaml fixture
    'moderator': '123',
    'reader': '123',
    'writer': '123',
}

class ListTest(TestCase):
    fixtures = ('movies.yaml',)
    list_url = reverse('list')
    
    def setUp(self):
        self.client.login(username='moderator', password=USER_PASSWORDS['moderator'])
        
    def get_response(self, **request_params):
        response = self.client.get(self.list_url + '?' + urlencode(request_params))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('object_list' in response.context)
        return response

    def test_search_results(self):
        # check empty results
        response = self.get_response(search='abracadabra')
        self.assertFalse(response.context['object_list'])
        self.assertContains(response, 'abracadabra')
        
        # check one word search
        response = self.get_response(search='serial')
        self.assertTrue(len(response.context['object_list']) == 2)

        # check one word search
        response = self.get_response(search='serial b')
        self.assertTrue(len(response.context['object_list']) == 1)

class PermissionsTest(TestCase):
    fixtures = ('movies.yaml',)

    def setUp(self):
        movie = self.movie = Movie.objects.all()[0]
        self.urls = {
            'list': reverse('list'),
            'add': reverse('add'),
            'delete': reverse('delete', kwargs={'pk': movie.pk}),
            'details': reverse('details', kwargs={'pk': movie.pk}),
            'edit_basic_info': reverse('edit_basic_info', kwargs={'pk': movie.pk}),
        }

    def get_response(self, url, username=None):
        if username:
            self.client.login(username=username, password=USER_PASSWORDS[username])
        else:
            self.client.logout()
        return self.client.get(url)
    
    def test_view_permissions(self):
        'fast check for views permissions'

        # maps page name to (username, status_code) pairs
        permissions = {
            'list' : {
                'moderator': 200,
                'reader': 200,
                'writer': 200,
                None: 302,
            },
            'add' : {
                'moderator': 200,
                'reader': 302,
                'writer': 200,
                None: 302,
            },
            'delete' : {
                'moderator': 200,
                'reader': 302,
                'writer': 302,
                None: 302,
            },
            'details' : {
                'moderator': 200,
                'reader': 200,
                'writer': 200,
                None: 302,
            },
            'edit_basic_info' : {
                'moderator': 200,
                'reader': 302,
                'writer': 200,
                None: 302,
            },
        }
        assert_message = "Wrong status code %s for page '%s', user '%s'"
        
        for url_name, scheme in permissions.items():
            for username, status_code in scheme.items():
                response = self.get_response(self.urls[url_name], username)
                self.assertEqual(response.status_code, status_code, assert_message % (response.status_code, url_name, username))

    def test_page_controls(self):
        'check for specific controls on html pages'
        
        # pairs (url_name, username, required_urls, stop_urls)
        urls = self.urls
        controls = (
            ('list', 'moderator', (urls['details'], urls['edit_basic_info'], urls['delete'], urls['add']), tuple()),
            ('list', 'writer', (urls['details'], urls['edit_basic_info'], urls['add']), (urls['delete'],)),
            ('list', 'reader', (urls['details'],), (urls['edit_basic_info'], urls['delete'], urls['add'])),            
            ('details', 'moderator', (urls['edit_basic_info'],), tuple()),
            ('details', 'writer', (urls['edit_basic_info'],), tuple()),
            ('details', 'reader', tuple(), (urls['edit_basic_info'],)),
        )
        assert_message = 'URL "%s" was not found on page "%s", user "%s"'
        
        for url_name, username, required_urls, stop_urls in controls:
            response = self.get_response(urls[url_name], username)
            for url in required_urls:
                self.assertContains(response, '"%s"' % url, msg_prefix=assert_message % (url, url_name, username))
            for url in stop_urls:
                self.assertNotContains(response, '"%s"' % url, msg_prefix=assert_message % (url, url_name, username))

class BaseChangeTest(TestCase):
    fixtures = ('movies.yaml',)

    def setUp(self):
        self.start_movie_count = Movie.objects.all().count()
        self.movie = Movie.objects.all()[0]
        self.client.login(username='moderator', password=USER_PASSWORDS['moderator'])

class DeleteTest(BaseChangeTest):

    def test_deletion(self):
        response = self.client.post(reverse('delete', kwargs={'pk': self.movie.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.start_movie_count-1, Movie.objects.all().count())

class AddTest(BaseChangeTest):
    pass
#    TODO
#    def test_add(self):
#        response = self.client.post(reverse('add'), data={
#        
#        })
#        self.assertEqual(response.status_code, 302)
#        self.assertEqual(self.start_movie_count+1, Movie.objects.all().count())
