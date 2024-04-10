from rest_framework import serializers
from ...models import Bookings, Users, Tables, UserTokens
from ..tables.serializers import  TableSerializer
from ..users.serializers import UserSerializer
from django.utils import timezone

class BookingSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Users.objects.all(),
        source='user'
    )
    table_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Tables.objects.all(),
        source='table'
    )
    user = UserSerializer(read_only=True)
    table = TableSerializer(read_only=True)

    class Meta:
        model = Bookings
        fields = ['id', 'user', 'table', 'persons', 'date', 'comment', 'user_id', 'table_id']

class ClientBookingSerializer(serializers.ModelSerializer):
    table_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Tables.objects.all(),
        source='table'
    )

    class Meta:
        model = Bookings
        fields = ['id', 'table_id', 'persons', 'date', 'comment']

    def create(self, validated_data):
        request = self.context.get('request')
        token = request.COOKIES.get('token')
        user_token = UserTokens.objects.filter(token=token, expiration_date__gt=timezone.now()).first()
        if not user_token:
            raise serializers.ValidationError('Token is invalid or has expired')
        validated_data['user'] = user_token.user
        booking = Bookings.objects.create(**validated_data)
        return booking

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['table'] = TableSerializer(instance.table).data
        return representation
