from django.db.models.aggregates import Count
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Artist, Album, Track
from .serializers import ArtistSerializer, AlbumSerializer, TrackSerializer
from .pagination import DefaultPagination
from .permissions import IsAdminOrReadOnly

# Create your views here.


class ArtistViewSet(ModelViewSet):
    queryset = Artist.objects.prefetch_related('tracks', 'albums')
    serializer_class = ArtistSerializer
    permission_classes = [IsAdminOrReadOnly]


class AlbumViewSet(ModelViewSet):
    queryset = Album.objects.annotate(
        tracks_count=Count('tracks')).select_related('artist'
            ).prefetch_related('tracks')
    serializer_class = AlbumSerializer
    permission_classes = [IsAdminOrReadOnly]


class TrackViewSet(ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    # pagination_class = DefaultPagination    # Optional pagination for tracks
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=True, methods=['GET'])
    def listen(self, request, pk):
        if self.get_queryset().filter(pk=pk).exists():
            return Response('{ “message”: “Here’s your music” }')
        raise NotFound
