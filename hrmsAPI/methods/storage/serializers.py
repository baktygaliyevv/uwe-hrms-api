from rest_framework import serializers
from ...models import RestaurantProducts
from ..restaurants.serializers import RestaurantSerializer
from ..products.serializers import ProductSerializer

class RestaurantProductsSerializer(serializers.ModelSerializer):
    
    restaurant = RestaurantSerializer(read_only = True)

    product = ProductSerializer(read_only = True)
    
    class Meta:
        model = RestaurantProducts
        fields = ['restaurant','product','count']

class RestaurantProductIncDecSerializer(serializers.ModelSerializer):

    restaurant_id = serializers.IntegerField()

    product_id = serializers.IntegerField()

    class Meta:
        model = RestaurantProducts
        fields = ['restaurant_id','product_id']