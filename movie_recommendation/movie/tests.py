from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Movie, Rating, User

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

