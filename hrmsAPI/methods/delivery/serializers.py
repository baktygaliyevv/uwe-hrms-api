from rest_framework import serializers
from ...models import Deliveries, DeliveryMenu, Users, Restaurants, Promocodes
from ..menu.serializers import MenuSerializer
from ..users.serializers import UserSerializer
from ..promocodes.serializers import PromocodeSerializer
from ..restaurants.serializers import RestaurantSerializer
#from ..users.views import Users

class DeliveryMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryMenu
        fields = ['id', 'delivery', 'menu', 'quantity']

# class DeliverySerializer(serializers.ModelSerializer):
#     user = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())
#     promocode = serializers.PrimaryKeyRelatedField(queryset=Promocodes.objects.all())
#     restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurants.objects.all())    
#     items = serializers.SerializerMethodField()
#     class Meta:
#         model = Deliveries
#         fields = ['id', 'user', 'restaurant', 'promocode', 'address', 'created_at', 'status', 'items']
class DeliveryCreateUpdateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())
    promocode = serializers.PrimaryKeyRelatedField(queryset=Promocodes.objects.all())
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurants.objects.all())
    items = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Deliveries
        fields = ['id', 'user', 'restaurant', 'promocode', 'address', 'created_at', 'status', 'items'] 

    def get_items(self, obj):
        delivery_menus = DeliveryMenu.objects.filter(delivery=obj).select_related('menu')
        items_data = []
        for delivery_menu in delivery_menus:
            item_data = {
                'item': MenuSerializer(delivery_menu.menu).data,
                'quantity': delivery_menu.quantity
            }
            items_data.append(item_data)
        return items_data  
    
class DeliveryReadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    promocode = PromocodeSerializer(read_only=True)
    restaurant = RestaurantSerializer(read_only=True)
    items = serializers.SerializerMethodField(read_only=True)

    def get_items(self, obj):
        delivery_menus = DeliveryMenu.objects.filter(delivery=obj).select_related('menu')
        items_data = []
        for delivery_menu in delivery_menus:
            item_data = {
                'item': MenuSerializer(delivery_menu.menu).data,
                'quantity': delivery_menu.quantity
            }
            items_data.append(item_data)
        return items_data
    
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
    
    class Meta:
        model = Deliveries
        fields = ['id', 'user', 'restaurant', 'promocode', 'address', 'created_at', 'status', 'items']