from django.urls import path
from rest_framework import routers
from .views import AlbumViewSet, ArtistViewSet, TrackViewSet, CustomerViewSet,\
    OrderViewSet, SearchView

router = routers.DefaultRouter()
router.register(r'album', AlbumViewSet, basename='albums')
router.register(r'artist', ArtistViewSet, basename='artists')
router.register(r'track', TrackViewSet, basename='tracks')
router.register(r'customer', CustomerViewSet, basename='customers')
router.register(r'subscription', OrderViewSet, basename='orders')

urlpatterns = [
    path('search/', SearchView.as_view()),
    # path('artist/<int:pk>', ArtistDetails.as_view(), name='artist-detail')
]
urlpatterns += router.urls
