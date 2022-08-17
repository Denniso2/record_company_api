from django.db import models


# Create your models here.


class Artist(models.Model):
    name = models.CharField(max_length=31)
    description = models.TextField()  # Depending on use case CharField may be appropriate

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']


class Album(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='artists')

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Track(models.Model):
    title = models.CharField(max_length=255)
    lyrics = models.TextField(null=True, blank=True)
    track_duration = models.CharField(max_length=255)  # Depending on use case DurationField may be appropriate
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='artists')
    album = models.ForeignKey(
        Album, on_delete=models.RESTRICT, related_name='tracks')

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']
