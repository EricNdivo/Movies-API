from rest_framework import status, generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .models import Rating, Movie  
from .serializers import MovieSerializer, RatingSerializer, FollowSerializer
import numpy as np
from .models import Movie, Rating, Follow
from sklearn.neighbors import NearestNeighbors
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.tokens import default_token_generator
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .tasks import fetch_new_movies

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

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

class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

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
            recommended_movies = Movie.objects.all().order_by('?')[:10]  
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
            movie_ratings.append([movie.id, movie.average_rating])

        movie_ratings_matrix = np.array(movie_ratings)
        knn = NearestNeighbors(n_neighbors=5)  
        knn.fit(movie_ratings_matrix)
        similar_movies = []
        for neighbors in knn.kneighbors(movie_ratings_matrix):
            similar_movies.extend([neighbor for neighbor in neighbors[1] if neighbor != movie.id])

        return similar_movies

class TopRatedMoviesViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'], url_path='top-rated', url_name='top-rated')
    def top_rated(self, request):
        top_rated_movies = Movie.objects.annotate(average_rating=Avg('rating__rating')).order_by('-average_rating')[:10]
        serializer= MovieSerializer(top_rated_movies, many=True)
        return Response(serailizer.data)
        
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self,request, *args, **kwargs):
        user = request.user
        movie_id = request.data.get('movie_id')
        rating = request.data.get('rating')
        review = request.data.get('review')

        if not movie_id:
            return Response({'error':'movie_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            rating_obj, created = Rating.objects.update_or_create(
                user=user,
                movie_id=movie_id,
                defaults={'rating':rating, 'review':review}
            )
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status':'review created' if created else 'review updated'})

class GenreRecommendationViewSet(viewsets.ViewSet):
    def list(self, request, genre=None):
        if genre:
            recommended_movies= Movie.objects.filter(genre__icontains=genre)
        else:
            return Response({'error':'Genre not provided'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = MovieSerializer(recommended_movies, many=True)
        return Response(serializer.data)   

class MovieSearchViewSet(viewsets.ViewSet):
    def list(self, request):
        query = request.query_params.get('query', None)
        if query:
            movies = Movie.objects.filter(title__icontains=query)
        else:
            movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return response(serializer.data)

class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            token = defaul.token_generator.make_token(user)
            reset_link = f"{request.build_absolute_uri('/reset-password/')}?token={token}&email={email}"
            message = render_to_string('reset_password_email.html', {'reset_link': reset_link})
            send_mail('Password Reset', message, 'no-reply@mysite.com', [email])
        return Response({'message': 'If a user with that email exists, a password reset link has been sent'})

class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_objects(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        user.profile_picture = request.data.get('profile_picture')
        user.save()
        return Response(UserSerializer(user).data)

class EnhancedRecommendationViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, user_id=None):
        if not user_id:
            return Response({'error': 'Missing user ID'}, status=status.HTTP_400_BAD_REQUEST)

        user_watch_history = Rating.objects.filter(user_id=user_id).values_list('movie_id', flat=True)
        similar_movie_ids = self.get_similar_movie_based_on_history(user_watch_history)
        recommended_movies = Movie.objects.filter(pk__in=similar_movie_ids).exclude(pk__in=user_watch_history) 


        serializer = MovieSerializer(recommended_movies, many=True)
        return Response(serializer.data)

    def get_similar_movies_based_on_history(self, watched_movie_ids):
          return []

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='follow')
    def follow(self, request):
        followee_id = request.data.get('followee_id')
        followee = User.objects.get(id=followee_id)
        follow, created = Follow.objects.get_or_create(follower=request.user, followee=followee)
        return Response({'status': 'followed' if created else 'already following'})


    @action(detail=False, methods=['post'], url_path='unfollow')
    def unfollow(self, request):
        followee_id = request.data.get('followee_id')
        followee = User.objects.get(id=followee_id)
        Follow.objects.filter(follower=request.user, folowee=followee).delete()
        return Response({'status': 'unfollowed'})


class AdvancedMovieSearchViewSet(viewsets.ViewSet):
    def list(self, request):
        query = request.query_params.get('query', None)
        genre = request.query_params.get('genre', None)
        min_rating = request.query_params.get('min_rating', None)
        release_date = request.query_params.get('release_date', None)

        movies = Movie.objects.all()

        if query:
            movies = movies.filter(title__icontains=query)
        if query:
            movies = movies.filter(genre__icontains=genre)
        if min_rating:
            movies = movies.filter(rating__gte=min-rating)
        if release_date:
            movies = movies.filter(release_date__gte=release_date)


        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

class FetchNewMoviesView(APIView):
    def get(self, request):
        url = 'https://api.example.com/new-movies'
        response = requests.get(url)
        if response.status_code == 200:
            movies_data = response.json()
            for movie_data in movies_data:
                Movie.objects.update_or_create(
                    title=movie_data['title'],
                    defaults={
                        'description': movie_data['description'],
                        'release_date': movie_data['release_data'],
                    }
                )
            return Response({'status': 'success', 'data': movies_data}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error', 'message': 'Failed to fetch new movies'}, status=status.HTTP_400_BAD_REQUEST)


class FetchNewMoviesViewSet(APIView):
    def get(self, request):
        response = request.get(url)
        if response.status_code == 200:
            movies_data = response.json()
            for movie_data in movies_data:
                Movie.objects.update_or_create(
                    title=movie_data['title'],
                    defaults={
                        'description': movie_data['description'],
                        'release_date': movie_data['release_data'],
                    }
                )
            return Response({'status' :'success', 'data': movies_data}, status=status.HTP_200_OK)
        else:
            return Response9({'status': 'error', 'message': 'Failed to fetch new movies'}, status=status.HTTP_400_BAD_REQUEST)







