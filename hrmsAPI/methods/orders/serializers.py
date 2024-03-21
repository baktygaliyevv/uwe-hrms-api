from rest_framework import serializers
from ...models import Orders, OrderMenu, Menu
from ..tables.serializers import  TableSerializer
from ..promocodes.serializers import  PromocodeSerializer
from ..users.serializers import UserSerializer
from ..menu.serializers import MenuSerializer

class OrderMenuSerializer(serializers.ModelSerializer):
    
    menu = MenuSerializer(read_only=True,many=True)

    class Meta:
        model=OrderMenu
        fields=['id','order_id','menu','quantity']

class OrderSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    table = TableSerializer(read_only=True)

    promocode = PromocodeSerializer(read_only=True)

    items = serializers.SerializerMethodField()

    class Meta:
        model = Orders
        fields = ['id','user','table','promocode','created_at','complete_at','items']

    def get_items(self, obj):
        menus_ids = OrderMenu.objects.filter(order=obj).values_list('menu',flat=True)
        menu = Menu.objects.filter(id__in=menus_ids)
        return MenuSerializer(menu,many=True).data

    def create(self, validated_data):
        order_menu_data = validated_data.pop('order_menu')
        order = Orders.objects.create(**validated_data)
        for menu_data in order_menu_data:
            OrderMenu.objects.create(order=order, **menu_data)
        return order
