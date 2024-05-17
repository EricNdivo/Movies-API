from rest_framework import serializers
from .models import Movie, Rating, MovieType, MovieDuration

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieType
        fields = '__all__'
class MovieDurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieDuration
        fields = '__all_'