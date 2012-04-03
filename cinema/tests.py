"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from urllib import urlencode
from django.test import TestCase
from django.core.urlresolvers import reverse

class ListTest(TestCase):
    fixtures = ('movies_test1.yaml',)
    list_url = reverse('list')
    
    def setUp(self):
        self.client.login(username='anonymous', password='123')
        
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
