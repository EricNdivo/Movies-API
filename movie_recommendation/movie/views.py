from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .models import Rating, Movie  
from .serializers import MovieSerializer, RatingSerializer 
import numpy as np
from sklearn.neighbors import NearestNeighbors

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class RecommendationViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, user_id=None):
        if not user_id:
            return Response({'error': 'Missing user ID'}, status=status.HTTP_400_BAD_REQUEST)

        user_ratings = Rating.objects.filter(user_id=user_id)
        if not user_ratings.exists():
            recommended_movies = Movie.objects.all().order_by('?')[:10]  # Random sample of 10 movies
        else:
            rated_movie_ids = [rating.movie.id for rating in user_ratings]
            rated_movies = Movie.objects.filter(pk__in=rated_movie_ids)
            similar_movie_ids = self.get_similar_movies(rated_movies)
            recommended_movies = Movie.objects.filter(pk__in=similar_movie_ids).exclude(pk__in=rated_movie_ids)

        serializer = MovieSerializer(recommended_movies, many=True)
        return Response(serializer.data)

    def get_similar_movies(self, rated_movies):
        if not rated_movies:
            return []

        movie_ratings = []
        for movie in rated_movies:
            # Assuming ratings have a numerical value (replace with your logic)
            movie_ratings.append([movie.id, movie.average_rating])

        movie_ratings_matrix = np.array(movie_ratings)
        knn = NearestNeighbors(n_neighbors=5)  # Find 5 similar movies
        knn.fit(movie_ratings_matrix)

        # Get similar movies for each rated movie and return a flattened list
        similar_movies = []
        for neighbors in knn.kneighbors(movie_ratings_matrix):
            similar_movies.extend([neighbor for neighbor in neighbors[1] if neighbor != movie.id])

        return similar_movies
