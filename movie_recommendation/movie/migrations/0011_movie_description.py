# Generated by Django 4.2.7 on 2024-06-05 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0010_remove_movie_description_alter_movie_release_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='description',
            field=models.TextField(null=True),
        ),
    ]