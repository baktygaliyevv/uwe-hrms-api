from rest_framework import serializers
from ...models import Menu, MenuCategories, Products, MenuProducts

class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategories
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'name', 'vegan', 'vegetarian', 'gluten_free']

class MenuProductSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Products.objects.all(),
        source='product.id'
    )
    class Meta:
        model = MenuProducts
        fields = ['product']

class MenuSerializer(serializers.ModelSerializer):
    category = MenuCategorySerializer(read_only=True)
    products = MenuProductSerializer(many=True, read_only=True)
    class Meta:
        model = Menu
        fields = ['id', 'name', 'category', 'price', 'products']

    def create(self, validated_data):
        # здесь логика создания нового меню айтема и связывание продуктов с этим меню айтемом хз правильно ли сделал если че потом починим
        menu_products_data = validated_data.pop('menu_products')
        menu = Menu.objects.create(**validated_data)
        for product_data in menu_products_data:
            MenuProducts.objects.create(menu=menu, **product_data)
        return menu
