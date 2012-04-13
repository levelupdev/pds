from django.test import TestCase
from django.core.urlresolvers import reverse

from utils import Movie, USER_PASSWORDS

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
