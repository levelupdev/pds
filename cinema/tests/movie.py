from urllib import urlencode

from django.test import TestCase
from django.core.urlresolvers import reverse

from utils import USER_PASSWORDS, Movie, BaseTest, BaseChangeTest

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

class DeleteTest(BaseTest):

    def test_deletion(self):
        response = self.client.post(reverse('delete', kwargs={'pk': self.movie.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.start_movie_count-1, Movie.objects.all().count())

class AddTest(BaseChangeTest):
    base_form_data = {
        'movie_type': 'tv',
        'title': 'Serial C',
        'provider': 'Distribber',
        'itunes_provider': 1,
        'metadata_language': 'en-US',
        'vendor_id': '129834IUH',
        'origin_country': 'US',
        'original_locale': 'en-us',
        'copyright': '2012 Distribber',
        'production_company': 'Distribber Yearof',
        'theatrical_release_date': '1970-10-02',
        'synopsis': 'This is a great movie',
        'next': True,
    }
    url = reverse('add')
    
    def test_add(self):
        # incorrect input
        data = self.base_form_data.copy()
        del data['movie_type']
        data['theatrical_release_date'] = '1970'
        incorrect_fields = ('movie_type', 'theatrical_release_date')
        
        # check for error messages on the page
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        form = response.context['form']
        for field_name in incorrect_fields:
            msg_prefix = "Incorrect '%s' input" % field_name
            self.assertTrue(form[field_name].errors)
         
            for error in form[field_name].errors:
                self.assertContains(response, error, msg_prefix = msg_prefix)
            
        # check for object creation
        data = self.base_form_data.copy()
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.start_movie_count+1, Movie.objects.all().count())

    def save_form_data(self, movie, **kwargs):
        data = self.base_form_data.copy()
        data['id'] = movie.id
        data.update(kwargs)
        return self.client.post(reverse('edit_basic_info', kwargs={'pk': movie.pk}), data)
