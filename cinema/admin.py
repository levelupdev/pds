from django.contrib import admin
from models import Movie, iTunesProvider, Territory, RatingSystem
from models import PriceTier, Rating, MovieRating, Genre, MovieGenre

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_complete',)

admin.site.register(Movie, MovieAdmin)
admin.site.register(iTunesProvider)
admin.site.register(Territory)
admin.site.register(RatingSystem)
admin.site.register(PriceTier)
admin.site.register(Rating)
admin.site.register(MovieRating)
admin.site.register(Genre)
admin.site.register(MovieGenre)
