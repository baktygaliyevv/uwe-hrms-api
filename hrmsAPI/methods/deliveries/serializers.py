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
    menu = serializers.SerializerMethodField()
    class Meta:
        model = Deliveries
        fields = ['id', 'user', 'restaurant', 'promocode', 'address', 'created_at', 'status', 'menu']

    def get_menu(self, obj):
        delivery_menus = DeliveryMenu.objects.filter(delivery=obj)
        menus = [dm.menu for dm in delivery_menus]
        return MenuSerializer(menus, many=True).data