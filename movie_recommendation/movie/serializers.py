from rest_framework import serializers
from .models import Movie, Rating, MovieType, MovieDuration
from django.contrib.auth.models import User
from .models import Movie, Rating, Follow
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user', 'movie', 'rating', 'review']

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieType
        fields = '__all__'
class MovieDurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieDuration
        fields = '__all_'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'profile_picture']
        extra_kwargs = {'password':{'write_only':True}}

        def create(self, validated_data):
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=valdated_data['password'],
                first_name=validated_data('first_name', ''),
                last_name=validated_data('last_name', ''),
            )
            return user
class MovieTypeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'

class FollowSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    followee = UserSerializer(read_only=True)


    class Meta:
        model = Follow
        fields = ['id', 'follower', 'followee']