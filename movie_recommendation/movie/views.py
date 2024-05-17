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
from rest_framework.views import APIView
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

class login(APIView):
    def get(self, request):
        if 'logged_in' in request.COOKIES and 'Access_Token' in request.COOKIES:
            context = {
                'Access_Token': request.COOKIES['Access_Token'],
                'logged_in':request.COOKIES.get('logged_in')
            }
            return render(request, 'abc.html', context)
        else:
            return render(request, 'login.html')
    def post(self,request,format=None):
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email,password)
        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password')

        refresh = RefreshTken.for_user(user)
        global ACCESS_TOKEN_GLOBAL
        ACCESS_TOKEN_GLOBAL=str(refresh.access_token)
        response=render(request, 'base.html')
        response.set_cookie('Acess_Token',str(refreh.access_token))
        response.set_cookie('logged_in',True)
        return response

class logout(APIView):
    def post(self, request):
        try:
            response=HttpResponseRedirect(reverse('login'))

            response.delete_cookie('Access_token')
            response.delete_cookie('login')
        except:
            return response({"status": status.HTTP_400_BAD_REQUEST})

def secret(APIView):
    pass