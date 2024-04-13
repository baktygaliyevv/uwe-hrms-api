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
    restaurant_id = serializers.IntegerField(required=True)
    promocode_id = serializers.CharField(allow_null = True, required=False)
    address = serializers.CharField(required=True)
    items = ItemSerializer(many=True)
    user_id = serializers.IntegerField(allow_null = True, required=False)
    created_at = serializers.DateTimeField(required = False)

    class Meta:
        model = Deliveries
        fields = ['restaurant_id', 'promocode_id', 'address',  'items', 'created_at', 'user_id'] 
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        validated_data['created_at'] = timezone.now()
        validated_data['status'] = 'new'
        delivery = Deliveries.objects.create(**validated_data)
        for item_data in items_data:
            menu_id = item_data.pop('item_id')
            DeliveryMenu.objects.create(delivery=delivery, menu_id=menu_id, **item_data)
        return delivery

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
        fields = ['id', 'restaurant', 'promocode', 'address', 'created_at', 'status', 'items', 'user']

class DeliveryCreateUpdateClientSerilizer(serializers.ModelSerializer):
    restaurant_id = serializers.IntegerField(required=True)
    promocode_id = serializers.CharField(allow_null = True, required=False)
    address = serializers.CharField(required=True)
    items = ItemSerializer(many = True)
    email = serializers.CharField(allow_null = True, required = False)
    first_name = serializers.CharField(required=True)
    last_name= serializers.CharField(required=True)
    created_at = serializers.DateTimeField(required = False)
    user_id = serializers.IntegerField(required=False)

    class Meta:
        model = Deliveries
        fields = ['restaurant_id', 'promocode_id', 'address', 'items', 'email', 'first_name', 'last_name', 'created_at', 'user_id']
    
    def create(self, validated_data):
        request = self.context.get('request')

        if validated_data.get('email')==None:
            flag = False
        else:
            flag = True
        flag2 = 'token' in request.COOKIES
            
        if(not flag and not flag2):
            return Response()
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
            validated_data['user_id'] = user.id

        validated_data['created_at'] = timezone.now()
        validated_data['status'] = 'new'
        items_data = validated_data.pop('items')
        delivery = Deliveries.objects.create(**validated_data)
        for item_data in items_data:
            menu_id = item_data.pop('item_id')
            DeliveryMenu.objects.create(delivery=delivery, menu_id=menu_id, **item_data)
        return delivery

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

class DeliveryEditDeleteSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(allow_null=True)
    restaurant_id = serializers.IntegerField(required=True)
    promocode_id = serializers.CharField(required=True)
    status = serializers.CharField(required=True)

    class Meta:
        model = Deliveries
        fields = ['user_id','restaurant_id','promocode_id','status']
    
    def destroy(self, validated_data):
        items_data = validated_data.pop('items')
        order = Deliveries.objects.delete(**validated_data)
        for menu_data in items_data:
            DeliveryMenu.objects.delete(order=order, **menu_data)
        return Response({
                'status':'Ok', 
            })
    