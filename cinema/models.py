from django.db import models
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from django_extensions.db.models import TimeStampedModel

class iTunesProvider(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta():
        verbose_name = 'iTunes Provider'
        verbose_name_plural = 'iTunes Providers'
    
class Movie(TimeStampedModel):
    MOVIE_TYPES = {'film':'Film', 'tv':'Tv', 'asset':'Asset'}.items()

    movie_type = models.CharField(max_length=10, choices = MOVIE_TYPES)
    title = models.CharField(max_length=100)
    provider = models.CharField(max_length=100, blank=True)
    itunes_provider = models.ForeignKey(iTunesProvider, null=True, blank=True)
    
    metadata_language = models.CharField(max_length=100, blank=True)
    vendor_id = models.CharField(max_length=100, blank=True)
    origin_country = models.CharField(max_length=100, blank=True)
    original_locale = models.CharField(max_length=100, blank=True, help_text = 'Original spoken locale of movie')
    copyright = models.CharField(max_length=100, blank=True)
    production_company = models.CharField(max_length=100, blank=True)
    theatrical_release_date_NA = models.BooleanField(default=True)
    theatrical_release_date = models.DateField(null=True, blank=True)
    synopsis = models.TextField(blank=True)
    
    is_complete = models.BooleanField(default=False)
    
    created_by = models.ForeignKey(User, related_name='created_records')
    modified_by = models.ForeignKey(User, related_name='modified_records')
    
    def get_absolute_url(self):
        return reverse('details', kwargs={'pk': self.pk})
    
    def __unicode__(self):
        return self.title

def enumerable_model_factory(name):
    class BaseEnumerable(models.Model):
        title = models.CharField(max_length = 100, primary_key=True)
        
        class Meta:
            ordering = 'title'
            abstract = True

        def __unicode__(self):
            return self.title
    class Meta:
        app_label = 'cinema'

    return type(name, (BaseEnumerable,), {'__module__': '', 'Meta': Meta})

Territory = enumerable_model_factory('Territory')
RatingSystem = enumerable_model_factory('RatingSystem')
PriceTier = enumerable_model_factory('PriceTier')

class Rating(models.Model):
    value = models.CharField(max_length = 100)
    system = models.ForeignKey(RatingSystem)
    
    class Meta:
        unique_together = ( ('value', 'system'), )

    def __unicode__(self):
        return self.value + ' - ' + self.system_id

class MovieRating(models.Model):
    movie = models.ForeignKey(Movie, related_name='ratings')
    rating = models.ForeignKey(Rating)
    territory = models.ForeignKey(Territory)
    reason = models.CharField(max_length = 100, blank=True)
    price_tier = models.ForeignKey(PriceTier)
    
    def __unicode__(self):
        return '%s - %s (rating=%s, related for=%s, Price Tier=%s)' % (
            self.movie, self.territory_id, self.rating, self.reason, self.price_tier_id)

Genre = enumerable_model_factory('Genre')

class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, related_name='genres')
    genre = models.ForeignKey(Genre)

    def __unicode__(self):
        return unicode(self.movie) + ' - ' + self.genre_id
