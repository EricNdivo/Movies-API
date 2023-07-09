from rest_framework import serializers
from .models import Movie, Rating, comment

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class commentSerializer(serializers. ModelSerializer):
    class Meta:
        model = comment
        fields = '__all__'