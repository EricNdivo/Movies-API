from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from movie.views import (
    MovieViewSet, RatingViewSet, CustomAuthToken, RecommendationViewSet, ProfileView, 
    RegisterView, TopRatedMoviesViewSet, GenreRecommendationViewSet, ReviewViewSet, 
    MovieSearchViewSet, FollowViewSet, AdvancedMovieSearchViewSet, 
    EnhancedRecommendationViewSet, PasswordResetView, FetchNewMoviesView
)

router = routers.DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'ratings', RatingViewSet)
router.register(r'recommendations', RecommendationViewSet, basename='recommendation')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'genre-recommendations', GenreRecommendationViewSet, basename='genre-recommendation')
router.register(r'top-rated', TopRatedMoviesViewSet, basename='top-rated')
router.register(r'moviereviews', ReviewViewSet, basename='moviereview')
router.register(r'follow', FollowViewSet, basename='follow')
router.register(r'advanced-search', AdvancedMovieSearchViewSet, basename='enhanced-recommendation')
router.register(r'enhanced-recommendations', EnhancedRecommendationViewSet, basename='enhanced-recomendation')
router.register(r'search', MovieSearchViewSet, basename='movie-search')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token/', CustomAuthToken.as_view(), name='api-token'),
    path('api/movies/', MovieViewSet.as_view({'get': 'list', 'post': 'create'}), name='movie-list'),
    path('api/movies/<int:pk>/', MovieViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='movie-detail'),
    path('api/ratings/', RatingViewSet.as_view({'get': 'list', 'post': 'create'}), name='rating-list'),
    path('api/ratings/<int:pk>/', RatingViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='rating-detail'),
    path('api/recommendations/<int:user_id>/', RecommendationViewSet.as_view({'get': 'list'}), name='recommendation-list'),
    path('api/genre-recommendations/<str:genre>/', GenreRecommendationViewSet.as_view({'get': 'list'}), name='genre-recommendation-list'),
    path('api/top-rated/', TopRatedMoviesViewSet.as_view({'get': 'list'}), name='recommendation-list'),
    path('api/profile', ProfileView.as_view(), name='profile'),
    path('api/register', RegisterView.as_view(), name='register'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('fetch-new-movies/', FetchNewMoviesView.as_view(), name='fetch-new-movies'),
]
