from rest_framework import serializers
from ...models import Restaurants

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model=Restaurants
        fields=['id','city']