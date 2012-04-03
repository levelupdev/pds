from django.contrib import admin
from models import Movie, iTunesProvider

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_complete',)

admin.site.register(Movie, MovieAdmin)
admin.site.register(iTunesProvider)
