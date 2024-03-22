from rest_framework import serializers
from ...models import Tables
from ..restaurants.serializers import RestaurantSerializer

class TableSerializer(serializers.ModelSerializer):

    restaurant = RestaurantSerializer(read_only=True)

    class Meta:
        model = Tables
        fields = ('id', 'restaurant', 'capacity')