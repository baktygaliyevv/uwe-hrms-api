from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from ...models import Deliveries, DeliveryMenu, Users, Restaurants, Promocodes, Menu, UserTokens
from ..menu.serializers import MenuSerializer
from ..users.serializers import UserSerializer
from ..promocodes.serializers import PromocodeSerializer
from ..restaurants.serializers import RestaurantSerializer
from ..orders.serializers import ItemSerializer
from django.utils import timezone
#from ..users.views import Users

class DeliveryMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryMenu
        fields = ['id', 'delivery', 'menu', 'quantity']

class DeliveryCreateUpdateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())
    promocode = serializers.PrimaryKeyRelatedField(queryset=Promocodes.objects.all())
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurants.objects.all())
    menu = serializers.PrimaryKeyRelatedField(queryset=Menu.objects.all())
    items = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Deliveries
        fields = ['id', 'user', 'restaurant', 'promocode', 'address', 'created_at', 'status', 'items', 'menu'] 
    
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
    
    class Meta:
        model = Deliveries
        fields = ['id', 'user', 'restaurant', 'promocode', 'address', 'created_at', 'status', 'items']

class DeliveryReadClientSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = Deliveries
        fields = ['id', 'restaurant', 'promocode', 'address', 'created_at', 'status', 'items']

class DeliveryCreateUpdateClientSerilizer(serializers.ModelSerializer):
    restaurant = serializers.CharField(reqiured=True)
    promocode = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    items = ItemSerializer(many = True)
    email = serializers.CharField(allow_null = True, required = False)
    first_name = serializers.CharField(required=True)
    last_name= serializers.CharField(required=True)
    created_at = serializers.DateTimeField(required = False)
    user_id = serializers.IntegerField(required=False)
    class Meta:
        model = Deliveries
        fields = ['restaurant', 'promocode', 'address', 'items', 'email', 'first_name', 'last_name', 'created_at']
    
    def create(self, validated_data):
        request = self.context.get('request')

        if validated_data.get('email')==None:
            flag = False
        else:
            flag = True
        flag2 = 'token' in request.COOKIES
            
        if(not flag and not flag2):
            return Response({ "status": "Error", "payload": "Unauthorized" }, status=status.HTTP_400_BAD_REQUEST)
        elif((not flag and flag2) or (flag and flag2)):
            obj = UserTokens.objects.get(token=request.COOKIES['token'])
            validated_data['user_id'] = UserSerializer(obj.user).data.get('id')
            validated_data.pop('first_name')
            validated_data.pop('last_name')
            if validated_data.get('email')!= None:
                validated_data.pop('email')
        else:
            user = Users.objects.create(
                first_name = validated_data.pop('first_name'),
                last_name = validated_data.pop('last_name'),
                email = validated_data.pop('email'),
                hash = None,
                salt = None,
                role = 'client',
                verified = 0
            )
            validated_data['user_id'] = user.objects.get('id')

        validated_data['created_at'] = timezone.now()
        items_data = validated_data.pop('items')
        order = Deliveries.objects.create(**validated_data)
        for item_data in items_data:
            menu_id = item_data.pop('item_id')
            DeliveryMenu.objects.create(order=order, menu_id=menu_id, **item_data)
        return order