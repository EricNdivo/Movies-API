# Generated by Django 4.2.7 on 2024-06-05 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0011_movie_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='release_year',
        ),
    ]
