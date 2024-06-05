from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    description = models.TextField(null=True)
    release_date = models.DateTimeField()
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
    review = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.movie} - {self.rating}'

class MovieType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    movie_type = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followee = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

