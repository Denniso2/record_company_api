from django.db import transaction
from rest_framework import serializers
import re
from datetime import datetime, date, timedelta
from .models import Artist, Album, Track, Customer, Order
from .signals import order_created
from django.contrib.auth.models import Group


class SimpleArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name', 'genre']


class SimpleAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['id', 'title']


class SimpleTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'title', 'track_duration']


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'title', 'lyrics', 'track_duration', 'album', 'artist']

    def validate_track_duration(self, value):
        try:
            datetime.strptime(value, '%M:%S')
            return value
        except ValueError:
            raise serializers.ValidationError("Incorrect duration format")


class ArtistSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    albums = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Artist
        fields = ['id', 'name', 'description', 'genre', 'albums', 'tracks']


class AlbumSerializer(serializers.ModelSerializer):
    album_type = serializers.SerializerMethodField(
        method_name='select_album_type'
    )
    tracks = SimpleTrackSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ['id', 'title', 'album_type', 'description', 'artist', 'tracks']

    def select_album_type(self, album):
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


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    orders = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'orders']


class CreateOrderSerializer(serializers.Serializer):
    SUBSCRIPTION_MONTHLY = 'M'
    SUBSCRIPTION_6_MONTH = 'H'  # From half year
    SUBSCRIPTION_YEARLY = 'Y'

    SUBSCRIPTION_CHOICES = [
        (SUBSCRIPTION_MONTHLY, 'Monthly'),
        (SUBSCRIPTION_6_MONTH, 'Semi annually'),
        (SUBSCRIPTION_YEARLY, 'Annually')
    ]

    subscription_type = serializers.ChoiceField(choices=SUBSCRIPTION_CHOICES)
    cc_number = serializers.CharField(max_length=19, write_only=True)
    cc_expiry_date = serializers.CharField(max_length=5, write_only=True)
    cc_holder_name = serializers.CharField(max_length=255, write_only=True)
    cc_cvv = serializers.CharField(max_length=3, write_only=True)

    def validate_cc_number(self, value):
        if bool(re.match(r"\d{4}-\d{4}-\d{4}-\d{4}$", value)):
            return value
        raise serializers.ValidationError("Incorrect CC number format")

    def validate_cc_expiry_date(self, value):
        try:
            expiry = datetime.strptime(value, '%m/%y')
            now = datetime.now()
            if expiry > now:
                return value
            else:
                raise serializers.ValidationError("Card has expired")
        except ValueError:
            raise serializers.ValidationError("Incorrect duration format")

    def validate_cc_cvv(self, value):
        if bool(re.match(r"\d{3}$", value)):
            return value
        raise serializers.ValidationError("Incorrect CVV format")

    def save(self):
        with transaction.atomic():
            user = self.context['user']
            subscribed_group, created = Group.objects.get_or_create(name="Subscribed")
            user_exists = user.groups.filter(name='Subscribed').exists()
            if user_exists:
                raise serializers.ValidationError("Already subscribed")
            sub_type = self.validated_data['subscription_type']
            now = date.today()
            if sub_type == 'M':
                expiry = now + timedelta(days=30)
            elif sub_type == 'H':
                expiry = now + timedelta(days=180)
            elif sub_type == 'Y':
                expiry = now + timedelta(days=365)  # 5 extra
            customer = Customer.objects.get(
                user_id=user.id)

            # Do credit card logic here

            order = Order.objects.create(customer=customer
                                         , subscription_expiry_date=expiry)

            user.groups.add(subscribed_group)

            order_created.send_robust(self.__class__, order=order)

            return order
