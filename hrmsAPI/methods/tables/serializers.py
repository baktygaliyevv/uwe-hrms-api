from rest_framework import serializers
from ...models import Tables, Restaurants
from ..restaurants.serializers import RestaurantSerializer 

class TableSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer(read_only=True)
    restaurant_id = serializers.PrimaryKeyRelatedField(
        queryset=Restaurants.objects.all(), 
        source='restaurant',
        write_only=True
    )

    class Meta:
        model = Tables
        fields = ('id', 'restaurant', 'restaurant_id', 'capacity')

    def create(self, validated_data):
        return Tables.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.restaurant = validated_data.get('restaurant', instance.restaurant)
        instance.capacity = validated_data.get('capacity', instance.capacity)
        instance.save()
        return instance
