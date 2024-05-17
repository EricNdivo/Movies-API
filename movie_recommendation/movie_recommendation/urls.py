"""
URL configuration for movie_recommendation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from movie.views import MovieViewSet, RatingViewSet
from movie.views import CustomAuthToken, MovieViewSet, RatingViewSet, RecommendationViewSet
router = routers.DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'ratings', RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin',admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token/', CustomAuthToken.as_view(), name='api-token'),
    path('api/movies/', MovieViewSet.as_view({'get': 'list', 'post': 'create'}), name='movie-list'),
    path('api/movies/<int:pk>/', MovieViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='movie-detail'),
    path('api/ratings/', RatingViewSet.as_view({'get': 'list', 'post': 'create'}), name='rating-list'),
    path('api/ratings/<int:pk>/', RatingViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='rating-detail'),
    path('api/recommendations/<int:user_id>/', RecommendationViewSet.as_view({'get': 'list'}), name='recommendation-list'),
]
