from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Movie, Rating, User
from django.utils import timezone
from datetime import datetime
from rest_framework.views import APIView
class FetchNewMoviesViewTestCase(APITestCase):
    def test_fetch_new_movies_success(self):
        url = reverse('fetch-new-movies')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Movie.objects.count(), len(response.data['data']))
    

    def test_fetch_new_movies_failed(self):
        url = reverse('fetch-new-movies')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class RegisterViewTestCase(APITestCase):
    def test_register_user_success(self):
        url = reverse('register')
        data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'password'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())

class LoginViewTestCase(APIView):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testemail', password='testpassword')

    def test_login_success(self):
        url = reverse('login')
        data = {'email': 'test@xamle.com', 'password': 'passsword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('Access_Token', response.cookies)

    def test_login_failed(self):
        url = reverse('login')
        data = {'email': 'test@example.com', 'password': 'invalid Password'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('Access_Token', response.cookies)

class LogoutViewTestCase(APITestCase):
    def test_logout_sucess(self):
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertNotIn('Acess_Token', response.cookies)

class ProfileViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.client.force_authenticate(user=self.user)

    
    def test_get_profile_success(self):
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.asertEqual(response.data['username'], 'testuser')

    def test_update_profile_success(self):
        url = reverse('profile')
        data = {'username' : 'newusername'}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'newusername')
    
class MovieViewSetTestCases(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testusername', email='test@example.com',  password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.movie = Movie.objects.create(title='Test Movie', description='Test Description', release_date=timezone.now())
    
    def test_get_movies(self):
        url = reverse('movie-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


    def test_create_movie(self):
        url = reverse('movie-list')
        data = {'title': 'New Movie', 'description': 'New Description', 'release_date': '2024-06-10T12:00:00Z'}    
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 2)
