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
