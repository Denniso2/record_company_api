from django.db.models.aggregates import Count
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Artist, Album, Track, Customer, Order
from .permissions import IsAdminOrReadOnly, IsSubscribed
from .serializers import ArtistSerializer, AlbumSerializer, TrackSerializer, \
    CustomerSerializer, CreateOrderSerializer, OrderSerializer, SimpleAlbumSerializer, \
    SimpleArtistSerializer, SimpleTrackSerializer


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

    @action(detail=True, methods=['GET'], permission_classes=[IsSubscribed])
    def listen(self, request, pk):
        if self.get_queryset().filter(pk=pk).exists():
            return Response('{ “message”: “Here’s your music” }')
        raise NotFound


class CustomerView(ListAPIView):
    queryset = Customer.objects.prefetch_related('orders').all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        subscribed_group, created = Group.objects.get_or_create(name="Subscribed")
        user_exists = request.user.groups.filter(name='Subscribed').exists()
        serializer = CreateOrderSerializer(
            data=request.data,
            context={'user_id': self.request.user.id,
                     'user_exists': user_exists})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.request.user.groups.add(subscribed_group)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()

        customer_id = Customer.objects.only(
            'id').get(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)


class SearchView(APIView):
    def get(self, request):
        search_query = self.request.query_params.get('search')
        if search_query in [None, '']:
            return Response('Provide search query in format ?search=', status.HTTP_400_BAD_REQUEST)
        # Searching titles only
        artists_queryset = Artist.objects.filter(name__icontains=search_query).all()
        tracks_queryset = Track.objects.filter(title__icontains=search_query).all()
        albums_queryset = Album.objects.filter(title__icontains=search_query).all()
        artist_serializer = SimpleArtistSerializer(artists_queryset, many=True)
        tracks_serializer = SimpleTrackSerializer(tracks_queryset, many=True)
        albums_serializer = SimpleAlbumSerializer(albums_queryset, many=True)
        return Response(
            {'artists': artist_serializer.data, 'tracks': tracks_serializer.data, 'albums': albums_serializer.data})
