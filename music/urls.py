from django.urls import path
from rest_framework import routers
from .views import AlbumViewSet, ArtistViewSet, TrackViewSet

router = routers.DefaultRouter()
router.register(r'album', AlbumViewSet, basename='albums')
router.register(r'artist', ArtistViewSet, basename='artists')
router.register(r'track', TrackViewSet, basename='tracks')

urlpatterns = [
    # path('artist/', ArtistsList.as_view()),
    # path('artist/<int:pk>', ArtistDetails.as_view(), name='artist-detail')
]
urlpatterns += router.urls
