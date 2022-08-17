from rest_framework import serializers
from .models import Artist, Album, Track


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'title', 'lyrics', 'track_duration', 'album', 'artist']


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name', 'description', 'genre', 'albums', 'tracks']


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['id', 'title', 'album_type', 'description', 'artist', 'tracks']

    album_type = serializers.SerializerMethodField(
        method_name='select_album_type'
    )

    def select_album_type(self, album: Album):
        if not album.tracks_count:
            return
        if album.tracks_count == 1:
            return 'Single'
        elif album.tracks_count <= 3:
            return 'EP'
        else:
            return 'Album'
