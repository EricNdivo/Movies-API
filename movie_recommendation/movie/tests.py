from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token 
from .models import Movie, Rating, Follow

class CustomAuthTokenTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('api-token')

    def test_obtain_auth_token(self):
        data = {'username': 'testuser', 'password': 'testpassword'}
        response =  self.client.post(self.url, data, format='json')
        self.assertEqual(response.status-code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

class RegisterViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('register')

    def test_register_user(self):
        data = {'username': 'newuser', 'password': 'newpassword', 'email': 'newuser@example.com'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

class FetchNewMoviesViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('fetch-new-movies')

    def test_fetch_new_movies(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.data)
        self.assertIn('data', response.data)
class MovieViewSetTests(APITestCase):
    def setUp(self):
        self.movie = Movie.objects.create(title='Test Movie', description='Test Description', release_date='2023-01-01')
        self.url = reverse('movie-list')
    def test_list_movies(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class RatingViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.movie = Movie.objects.create(title='Test Movie', description='Test Description', release_date='2023-01-01')
        self.rating = Rating.objects.create(user=self.user, movie=self.movie, rating=5, review='Great movie')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_rating(self):
        url = reverse('rating-list')
        data = {'movie_id': self.movie.id, 'rating': 4, 'review': 'Good Movie'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    

class RecommendationViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client =APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('recommendation-list', kwargs={'user_id' : self.user.id})

    def test_get_recommendations(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TopRatedMoviesViewSetTests(APITestCase):
    def setUp(self):
        self.movie = Movie.objects.create(title='Test Movie', description='Test Description', release_date='2023-01-01')
        self.rating = Rating.objects.create(movie=self.movie, rating=5)
        self.url = reverse('top-rated')

    def test_top_rated_movies(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ReviewViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.movie = Movie.objects.create(title='Test Movie', description='test description', release_year='2023-01-01')
        self.rating = Rating.objects.create(user=self.user, movie=self.movie, rating=5, review='Great movie')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('review-list')


    def test_create_review(self):
        data = {'movie_id': self.movie.id, 'rating': 4, 'review': 'Good movie'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

