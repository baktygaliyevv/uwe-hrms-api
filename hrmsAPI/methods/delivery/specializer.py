from rest_framework import serializers
from ...models import Deliveries, DeliveryMenu

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Deliveries
        fields = ['id', 'user', 'restaurant', 'promocode', 'address', 'created_at', 'status']

class DeliveryMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryMenu
        fields = ['id', 'delivery', 'menu', 'quantity']