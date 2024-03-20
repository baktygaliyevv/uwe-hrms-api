from rest_framework import serializers
from ...models import OrderMenu, Menu
from ..menu.serializers import MenuSerializer

class OrderMenuSerializer(serializers.ModelSerializer):
    
    menu = MenuSerializer(read_only=True,many=True)

    class Meta:
        model=OrderMenu
        fields=['id','order_id','menu','quantity']

