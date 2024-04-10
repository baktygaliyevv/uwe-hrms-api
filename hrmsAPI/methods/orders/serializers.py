from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ...models import Orders, OrderMenu, Menu, Users, UserTokens
from ..tables.serializers import  TableSerializer
from ..promocodes.serializers import  PromocodeSerializer
from ..users.serializers import UserSerializer
from ..menu.serializers import MenuSerializer
from django.utils import timezone

class OrderMenuAddSerializer(serializers.ModelSerializer):
    item = MenuSerializer(read_only=True,many=True)
    item_id = serializers.IntegerField()

    class Meta:
        model = OrderMenu
        fields = ['item','item_id','quantity']

class OrderMenuEditDeleteSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField()

    class Meta:
        model = OrderMenu
        fields = ['quantity']

class MultipleFieldLookupMixin(object):
    def get_object(self):
        queryset = self.get_queryset()            
        queryset = self.filter_queryset(queryset) 
        filter = {}
        for field in self.lookup_fields:
            try:                                 
                filter[field] = self.kwargs[field]
            except Exception:
                pass
        return get_object_or_404(queryset, **filter)

class OrderGetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    table = TableSerializer(read_only=True)
    promocode = PromocodeSerializer(read_only=True)
    items = serializers.SerializerMethodField()

    class Meta:
        model = Orders
        fields = ['id','user','table','promocode','created_at','complete_at','items']

    def get_items(self, obj):
        menus_ids = OrderMenu.objects.filter(order=obj).values_list('menu',flat=True)
        menu_items = Menu.objects.filter(id__in=menus_ids)
        items_data = []
        for item in menu_items:
            order_menu = OrderMenu.objects.get(order=obj, menu=item)
            item_data = {
                'item': MenuSerializer(item).data,
                'quantity': order_menu.quantity
            }
            items_data.append(item_data)
        return items_data

class ItemSerializer(serializers.Serializer):
    item_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True)

class OrderAddSerializer(serializers.ModelSerializer):
    table_id = serializers.IntegerField(required=True)
    promocode_id = serializers.CharField(allow_null=True, required=True)
    items = ItemSerializer(many = True)
    user_id = serializers.IntegerField(required=True)
    created_at = serializers.DateTimeField(required = False)

    class Meta:
        model = Orders
        fields = ['table_id','promocode_id','items','user_id','created_at']
            
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        validated_data['created_at'] = timezone.now()
        order = Orders.objects.create(**validated_data)
        for item_data in items_data:
            menu_id = item_data.pop('item_id')
            OrderMenu.objects.create(order=order, menu_id=menu_id, **item_data)
        return order
    
class OrderEditDeleteSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(allow_null=True)
    table_id = serializers.IntegerField()
    promocode_id = serializers.CharField(allow_null=True)
    complete_at = serializers.DateTimeField(allow_null=True)

    class Meta:
        model = Orders
        fields = ['user_id','table_id','promocode_id','complete_at']
    
    def destroy(self, validated_data):
        items_data = validated_data.pop('items')
        order = Orders.objects.delete(**validated_data)
        for menu_data in items_data:
            OrderMenu.objects.delete(order=order, **menu_data)
        return Response({
                'status':'Ok', 
            }) 

class OrderGetClientSerializer(serializers.ModelSerializer):
    table = TableSerializer(read_only=True)
    promocode = PromocodeSerializer(read_only=True)
    items = serializers.SerializerMethodField()

    class Meta:
        model = Orders
        fields = ['id','table','promocode','created_at','complete_at','items']

    def get_items(self, obj):
        menus_ids = OrderMenu.objects.filter(order=obj).values_list('menu',flat=True)
        menu_items = Menu.objects.filter(id__in=menus_ids)
        items_data = []
        for item in menu_items:
            order_menu = OrderMenu.objects.get(order=obj, menu=item)
            item_data = {
                'item': MenuSerializer(item).data,
                'quantity': order_menu.quantity
            }
            items_data.append(item_data)
        return items_data

class OrderAddClientSerializer(serializers.ModelSerializer):
    table_id = serializers.IntegerField(required=True)
    promocode_id = serializers.CharField(required=True)
    items = ItemSerializer(many = True)
    email = serializers.CharField(allow_null = True, required = False)
    first_name = serializers.CharField(required=True)
    last_name= serializers.CharField(required=True)
    created_at = serializers.DateTimeField(required = False)
    user_id = serializers.IntegerField(required=False)

    class Meta:
        model = Orders
        fields = ['table_id','promocode_id','items','email','first_name','last_name','created_at','user_id']

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
        order = Orders.objects.create(**validated_data)
        for item_data in items_data:
            menu_id = item_data.pop('item_id')
            OrderMenu.objects.create(order=order, menu_id=menu_id, **item_data)
        return order