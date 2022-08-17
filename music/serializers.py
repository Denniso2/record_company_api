from rest_framework import serializers
import time
from .models import Artist, Album, Track



class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'title', 'lyrics', 'track_duration', 'album', 'artist']

    def validate_track_duration(self, value):
        try:
            time.strptime(value, '%M:%S')
            return value
        except ValueError:
            raise serializers.ValidationError("Incorrect duration format")


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name', 'description', 'genre', 'albums', 'tracks']


class AlbumSerializer(serializers.ModelSerializer):
    album_type = serializers.SerializerMethodField(
        method_name='select_album_type'
    )

    class Meta:
        model = Album
        fields = ['id', 'title', 'album_type', 'description', 'artist', 'tracks']

    def select_album_type(self, album: Album):
        try:
            if not album.tracks_count:
                return
            if album.tracks_count == 1:
                return 'Single'
            elif album.tracks_count <= 3:
                return 'EP'
            else:
                return 'Album'
        except AttributeError:
            return
