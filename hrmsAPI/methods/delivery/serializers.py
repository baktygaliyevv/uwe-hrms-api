from rest_framework import serializers
from ...models import Deliveries, DeliveryMenu, Users, Restaurants, Promocodes, Menu
from ..menu.serializers import MenuSerializer
from ..users.serializers import UserSerializer
from ..promocodes.serializers import PromocodeSerializer
from ..restaurants.serializers import RestaurantSerializer
#from ..users.views import Users

class DeliveryMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryMenu
        fields = ['id', 'delivery', 'menu', 'quantity']

class DeliveryUISerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    items = serializers.SerializerMethodField()
    #FIXME вопрос
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
        fields = ['email', 'first_name', 'last_name', 'restaurant', 'promocode', 'address', 'created_at', 'status', 'items']

    def create(self, validated_data):
        email = validated_data.pop('email', None)
        first_name = validated_data.pop('first_name', None)
        last_name = validated_data.pop('last_name', None)

        if email:
            user, created = Users.objects.get_or_create(email=email, defaults={
                'first_name': first_name,
                'last_name': last_name
                # другие поля пользователя, если необходимо
            })
            validated_data['user'] = user

        return Deliveries.objects.create(**validated_data)

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