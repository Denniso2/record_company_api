from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from .models import Artist, Album, Track
from django.db.models.aggregates import Count
from .serializers import ArtistSerializer, AlbumSerializer, TrackSerializer

# Create your views here.


class ArtistViewSet(ModelViewSet):
    queryset = Artist.objects.prefetch_related('tracks', 'albums')
    serializer_class = ArtistSerializer


class AlbumViewSet(ModelViewSet):
    queryset = Album.objects.annotate(
        tracks_count=Count('tracks')).select_related('artist'
            ).prefetch_related('tracks')
    serializer_class = AlbumSerializer


class TrackViewSet(ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
