from django import forms
from django.forms.models import inlineformset_factory

from models import Movie, MovieRating, MovieGenre

class BaseModelForm(forms.ModelForm):
    error_css_class = 'error'

class BasicInfo(BaseModelForm):
    def __init__(self, *args, **kwargs):
        super(BasicInfo, self).__init__(*args, **kwargs)
        self.fields['itunes_provider'].label = "Provider (for iTunes)"
        self.fields['itunes_provider'].help_text = 'For example, select "premiere" if provider is "Distribber"'
        self.fields['metadata_language'].label = "Language of Metadata"
        self.fields['vendor_id'].label = "Vendor ID"
        self.fields['origin_country'].label = "Country of Origin"
        self.fields['original_locale'].label = "Original Spoken Locale of Movie"
        self.fields['theatrical_release_date_NA'].label = "Check if N/A"
    
    class Meta:
        model = Movie
        fields = (
            'movie_type', 'title', 'provider', 'itunes_provider', 'metadata_language',
            'vendor_id', 'origin_country', 'original_locale', 'copyright',
            'production_company', 'theatrical_release_date_NA', 'theatrical_release_date', 'synopsis',
        )

class MovieRatingForm(BaseModelForm):
    class Meta:
        model = MovieRating

class MovieGenreForm(BaseModelForm):
    class Meta:
        model = MovieGenre

MovieRatingFormset = inlineformset_factory(parent_model=Movie, model=MovieRating, form=MovieRatingForm, extra=1)
MovieGenreFormset = inlineformset_factory(parent_model=Movie, model=MovieGenre, form=MovieGenreForm, max_num=3, extra=3)
