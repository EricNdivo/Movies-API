from django.contrib import admin
from .models import MovieType, Movie, Rating

admin.site.register(MovieType)
admin.site.register(Movie)
admin.site.register(Rating)