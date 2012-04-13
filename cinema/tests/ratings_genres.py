from django.test import TestCase
from django.core.urlresolvers import reverse

from utils import BaseChangeTest, USER_PASSWORDS, Movie

class RatingsGenresTest(BaseChangeTest):
    base_change_data = {
        'ratings-TOTAL_FORMS': 1,
        'ratings-INITIAL_FORMS': 1,
        'ratings-MAX_NUM_FORMS': '',
        
        'ratings-0-territory': 'US',
        'ratings-0-rating': 1,
        'ratings-0-reason': 'violence',
        'ratings-0-price_tier': 4,
        'ratings-0-DELETE': '',
        'ratings-0-movie': 1,
        'ratings-0-id': 1,
        
        'genres-TOTAL_FORMS': 1,
        'genres-INITIAL_FORMS': 1,
        'genres-MAX_NUM_FORMS': 3,
        
        'genres-0-genre': 'drama',
        'genres-0-movie': 1,
        'genres-0-id': 1,
        'genres-0-DELETE': '',

        'next': '',
    }
    
    base_add_data = base_change_data.copy()
    base_add_data.update({
        'ratings-TOTAL_FORMS': 2,
        
        'ratings-1-territory': 'CA',
        'ratings-1-rating': 2,
        'ratings-1-reason': '',
        'ratings-1-price_tier': 4,
        'ratings-1-DELETE': '',
        'ratings-1-movie': 1,
        'ratings-1-id': '',
        
        'genres-TOTAL_FORMS': 2,
        
        'genres-1-genre': 'drama',
        'genres-1-movie': 1,
        'genres-1-id': '',
    })
    
    def setUp(self):
        super(RatingsGenresTest, self).setUp()
        self.url = reverse('edit_rating_and_genre', kwargs={'pk': self.movie.pk})
        self.rating_start_count = self.movie.ratings.all().count()
        self.genre_start_count = self.movie.genres.all().count()

    def test_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('forms' in response.context)
        forms = response.context['forms']

        self.assertTrue('ratings' in forms and 'genres' in forms)
        self.assertEqual(len(forms['ratings'].initial_forms), 2)
        self.assertEqual(len(forms['genres'].initial_forms), 2)

        for phrase in ('violence', 'US', 'CA', 'drama', 'comedy'):
            self.assertContains(response, phrase)

    def test_append(self):
        data = self.base_add_data.copy()
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.rating_start_count+1, self.movie.ratings.all().count())
        self.assertEqual(self.genre_start_count+1, self.movie.genres.all().count())        
    
    def test_incorrect_append(self):
        # incorrect input
        data = self.base_add_data.copy()
        del data['ratings-1-territory']
        del data['genres-1-genre']

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_change(self):
        data = self.base_change_data.copy()
        data['ratings-0-reason'] = 'abracadabra'
        data['genres-0-genre'] = 'comedy'
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.rating_start_count, self.movie.ratings.all().count())
        self.assertEqual(self.genre_start_count, self.movie.genres.all().count())
        
        self.assertEqual(self.movie.ratings.filter(reason = 'abracadabra').count(), 1)
        self.assertEqual(self.movie.ratings.filter(reason = 'violence').count(), 0)

        self.assertEqual(self.movie.genres.filter(genre = 'comedy').count(), 2)
        self.assertEqual(self.movie.genres.filter(genre = 'drama').count(), 0)

    def test_incorrect_change(self):
        data = self.base_change_data.copy()
        del data['ratings-0-territory']
        del data['genres-0-genre']

        # edit by difer from default moderator user - we need to check 'modified_by' field        
        self.client.login(username='writer', password=USER_PASSWORDS['writer'])
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.movie = Movie.objects.get(pk = self.movie.pk)

        self.assertEqual(self.movie.created_by.username, 'moderator')
        self.assertEqual(self.movie.modified_by.username, 'writer')
        
        self.assertTrue('forms' in response.context)
        forms = response.context['forms']
        self.assertTrue('ratings' in forms and 'genres' in forms)

        self.assertTrue(forms['ratings'][0].errors and forms['genres'][0].errors)
        for msg in sum(forms['ratings'][0].errors.values() + forms['genres'][0].errors.values(), []):
            self.assertContains(response, msg)

        self.assertTrue('forms' in response.context)
        # incorrect_fields = ('ratings-1-territory', 'genres-1-genre')

    def test_deletion(self):
        data = self.base_change_data.copy()
        data['genres-0-DELETE'] = data['ratings-0-DELETE'] = 1
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.rating_start_count-1 == self.movie.ratings.all().count())
        self.assertTrue(self.genre_start_count-1 == self.movie.genres.all().count())

    def save_form_data(self, movie, **kwargs):
        data = self.base_change_data.copy()
        data['ratings-0-movie'] = movie.pk
        data['genres-0-id'] = movie.pk
        data.update(kwargs)
        return self.client.post(self.url, data)    
