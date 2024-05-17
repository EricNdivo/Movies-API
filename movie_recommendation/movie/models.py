from django.db import models
from django.contrib.auth.models import User  # Ensure to import User if you are using it in your models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    release_year = models.IntegerField()
    director = models.CharField(max_length=255)
    synopsis = models.TextField()
    duration = models.OneToOneField('MovieDuration', on_delete=models.CASCADE, null=True, blank=True, related_name='movie_duration')

    def __str__(self):
        return self.title

class MovieDuration(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE, related_name='duration_details')
    hours = models.PositiveIntegerField()
    minutes = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.hours}h {self.minutes}m"

    def total_minutes(self):
        return self.hours * 60 + self.minutes

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

class MovieType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    movie_type = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name
