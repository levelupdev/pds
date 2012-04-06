from django import forms

from models import Movie

class BaseMovieEdit(forms.ModelForm):
    def save(self, author):
        obj = super(BaseMovieEdit, self).save(commit=False)
        obj.modified_by = author
        obj.save()
        return obj
        
class BasicInfo(BaseMovieEdit):
    class Meta:
        model = Movie
        fields = (
            'movie_type', 'title', 'provider', 'itunes_provider', 'metadata_language',
            'vendor_id', 'origin_country', 'original_locale', 'copyright',
            'production_company', 'has_theatrical_release_date', 'theatrical_release_date', 'synopsis',
        )
