from django.db.models.aggregates import Count
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Artist, Album, Track, Customer, Order
from .permissions import IsAdminOrReadOnly
from .serializers import ArtistSerializer, AlbumSerializer, TrackSerializer, CustomerSerializer, CreateOrderSerializer, OrderSerializer


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


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    #permission_classes = [IsAdminUser]


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data,
            context={'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return OrderSerializer
