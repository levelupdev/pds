from django import forms

from models import Movie

class BaseMovieEdit(forms.ModelForm):
    error_css_class = 'error'
    
    def save(self, author, commit=True):
        obj = super(BaseMovieEdit, self).save(commit=False)

        obj.created_by = (obj.created_by_id and obj.created_by) or author
        obj.modified_by = author

        if commit:
            obj.save()

        return obj
        
class BasicInfo(BaseMovieEdit):
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
