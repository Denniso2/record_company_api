from django.urls import path
from rest_framework import routers
from .views import AlbumViewSet, ArtistViewSet, TrackViewSet, CustomerView,\
    OrderViewSet, SearchView

router = routers.DefaultRouter()
router.register(r'album', AlbumViewSet, basename='albums')
router.register(r'artist', ArtistViewSet, basename='artists')
router.register(r'track', TrackViewSet, basename='tracks')
router.register(r'subscription', OrderViewSet, basename='orders')

urlpatterns = [
    path('customer/', CustomerView.as_view()),
    path('search/', SearchView.as_view()),
]
urlpatterns += router.urls
