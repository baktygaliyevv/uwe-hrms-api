from rest_framework import serializers
from ..users.serializers import UserSerializer
from ..promocodes.serializers import PromocodeSerializer
from ...models import Deliveries, DeliveryMenu

class DeliverySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    promocode = PromocodeSerializer(read_only=True)
    class Meta:
        model = Deliveries
        fields = ['id', 'user', 'restaurant', 'promocode', 'address', 'created_at', 'status']

class DeliveryMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryMenu
        fields = ['id', 'delivery', 'menu', 'quantity']