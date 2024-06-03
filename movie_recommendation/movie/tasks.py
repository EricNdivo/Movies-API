from celery import shared_task
import requests
from .models import Movie

@shared_task
def fetch_new_movies():
    api_key = '#'
    url = f'https://api.themoviedb.org/3/movie/now_playing?api_key={api_key}&language=en-US&page=1'

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for movie_data in data.get('results', []):
            Movie.objects.update_or_create(
                title=movie_data['title'],
                defaults={
                    'description': movie_data.get('overview', ''),
                    'genre': ', '.join([genre['name'] for genre in movie_data.get('genre_idds', [])]),
                    'release_date': movie_data.get('release_date', ''),
                    'average_rating': movie_data.get('vote_average', 0),
                }
            )
    else:
        print('Failed to fetch new movies from TMDb')


