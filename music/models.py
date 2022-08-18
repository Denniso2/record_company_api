from django.db import models
from django.conf import settings


# Create your models here.


class Artist(models.Model):
    GENRE_POP = 'P'
    GENRE_ROCK = 'R'
    GENRE_METAL = 'M'
    GENRE_INDIE = 'I'
    GENRE_HOUSE = 'H'
    GENRE_TECHNO = 'T'

    GENRE_CHOICES = [
        (GENRE_POP, 'Pop'), (GENRE_ROCK, 'Rock'),
        (GENRE_METAL, 'Metal'), (GENRE_INDIE, 'Indie'),
        (GENRE_HOUSE, 'House'), (GENRE_TECHNO, 'Techno')
    ]
    name = models.CharField(max_length=31)
    description = models.TextField()  # Depending on use case CharField may be appropriate
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']


class Album(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name='albums')

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Track(models.Model):
    title = models.CharField(max_length=255)
    lyrics = models.TextField(null=True, blank=True)
    track_duration = models.CharField(
        max_length=255)  # Depending on use case DurationField may be appropriate
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name='tracks')
    album = models.ForeignKey(
        Album, on_delete=models.RESTRICT, related_name='tracks')

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
