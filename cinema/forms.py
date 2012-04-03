from django import forms

class BasicInfo(forms.ModelForm):
    class Meta:
        fields = (
            'movie_type', 'title', 'provider', 'itunes_provider', 'metadata_language'
            'vendor_id', 'origin_country', 'original_locale', 'copyright'
            'production_company', 'has_theatrical_release_date', 'theatrical_release_date', 'synopsis'
        )
