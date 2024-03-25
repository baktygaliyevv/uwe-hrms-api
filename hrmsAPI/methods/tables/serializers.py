from rest_framework import serializers
from ...models import Tables, Restaurants
from ..restaurants.serializers import RestaurantSerializer

class TableSerializer(serializers.ModelSerializer):
    restaurant_id = serializers.PrimaryKeyRelatedField(
        queryset=Restaurants.objects.all(), source='restaurant', write_only=True
    )

    class Meta:
        model = Tables
        fields = ('id', 'restaurant_id', 'capacity')