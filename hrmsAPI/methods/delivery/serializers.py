from rest_framework import serializers
from ..users.serializers import UserSerializer
from ..promocodes.serializers import PromocodeSerializer
from ...models import Deliveries, DeliveryMenu
from ..restaurants.serializers import RestaurantSerializer
from ..menu.serializers import MenuSerializer

class DeliveryMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryMenu
        fields = ['id', 'delivery', 'menu', 'quantity']

class DeliverySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    promocode = PromocodeSerializer(read_only=True)
    restaurant = RestaurantSerializer(read_only=True)    
    items = serializers.SerializerMethodField()
    class Meta:
        model = Deliveries
        fields = ['id', 'user', 'restaurant', 'promocode', 'address', 'created_at', 'status', 'items']

    # def get_items(self, obj):
    #     delivery_menus = DeliveryMenu.objects.filter(delivery=obj)
    #     menus = [dm.menu for dm in delivery_menus]
    #     return MenuSerializer(menus, many=True).data
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