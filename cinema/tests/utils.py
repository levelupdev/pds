from django.test import TestCase

from cinema.models import Movie

USER_PASSWORDS = { # for movies.yaml fixture
    'moderator': '123',
    'reader': '123',
    'writer': '123',
}

class BaseTest(TestCase):
    fixtures = ('movies.yaml',)

    def setUp(self):
        self.start_movie_count = Movie.objects.all().count()
        self.movie = Movie.objects.all()[0]
        self.client.login(username='moderator', password=USER_PASSWORDS['moderator'])

class BaseChangeTest(BaseTest):
    'Test for every add/edit form for movie object'

    def test_modified_created_by(self):
        'Tests modified_by field updates after saving form data'
        self.assertEqual(self.movie.modified_by.username, 'moderator')
        self.client.login(username='writer', password=USER_PASSWORDS['writer'])
        
        response = self.save_form_data(self.movie, next = '')
        self.assertEqual(response.status_code, 302)
        self.movie = Movie.objects.get(pk = self.movie.pk)
        
        self.assertEqual(self.movie.created_by.username, 'moderator')
        self.assertEqual(self.movie.modified_by.username, 'writer')
            
    def test_is_complete(self):
        'Tests is_complete field value after saving form data'
        
        self.movie.is_complete = False
        self.movie.save()

        response = self.save_form_data(self.movie, next='')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Movie.objects.get(pk = self.movie.pk).is_complete, False)

        response = self.save_form_data(self.movie, finish='')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Movie.objects.get(pk = self.movie.pk).is_complete, True)
    
        response = self.save_form_data(self.movie, next='')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Movie.objects.get(pk = self.movie.pk).is_complete, True)

    def save_form_data(self, movie, **kwargs):
        '''
        Correctly saves form data for movie object, returns response.
        kwargs is optional post params
        '''
        raise NotImplemented()
