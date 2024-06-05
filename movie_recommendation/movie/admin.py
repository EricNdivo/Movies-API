from django.contrib import admin
from .models import Profile, Movie, MovieDuration, Rating, MovieType, Follow

admin.site.register(Profile)
admin.site.register(Movie)
admin.site.register(MovieDuration)
admin.site.register(Rating)
admin.site.register(MovieType)
admin.site.register(Follow)