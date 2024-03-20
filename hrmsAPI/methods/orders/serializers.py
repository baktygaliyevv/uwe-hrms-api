from rest_framework import serializers
from ...models import Orders, OrderMenu
from ..tables.serializers import  TableSerializer
from ..promocodes.serializers import  PromocodeSerializer
from ..users.serializers import UserSerializer
from ..orderMenu.serializers import OrderMenuSerializer

class OrderSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    table = TableSerializer(read_only=True)

    promocode = PromocodeSerializer(read_only=True)

    class Meta:
        model = Orders
        fields = ['id','user','table','promocode','created_at','complete_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['items'] = OrderMenuSerializer(read_only=True,many=True).data
        return data

    def create(self, validated_data):
        order_menu_data = validated_data.pop('order_menu')
        order = Orders.objects.create(**validated_data)
        for menu_data in order_menu_data:
            OrderMenu.objects.create(order=order, **menu_data)
        return order
