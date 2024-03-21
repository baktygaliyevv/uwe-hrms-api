from rest_framework import serializers
from ...models import Menu, MenuCategories, Products, MenuProducts

class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategories
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    vegan = serializers.BooleanField()
    vegetarian = serializers.BooleanField()
    gluten_free = serializers.BooleanField()

    class Meta:
        model = Products
        fields = ['id', 'name', 'vegan', 'vegetarian', 'gluten_free']

    def to_representation(self, instance):
        representation = super(ProductSerializer, self).to_representation(instance)
        representation['vegan'] = bool(instance.vegan)
        representation['vegetarian'] = bool(instance.vegetarian)
        representation['gluten_free'] = bool(instance.gluten_free)
        return representation

class MenuProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = MenuProducts
        fields = ['product']

class MenuSerializer(serializers.ModelSerializer):
    category = MenuCategorySerializer(read_only=True, source='menu_category')
    # products = MenuProductSerializer(many=True, read_only=True, source='menu')
    products = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ['id', 'name', 'category', 'price', 'products']

    def get_products(self, obj):
        # Get all MenuProducts for this menu
        menu_products = MenuProducts.objects.filter(menu=obj)
        # Now get the related Products from the menu_products query
        product_ids = menu_products.values_list('product', flat=True)
        products = Products.objects.filter(id__in=product_ids)
        return ProductSerializer(products, many=True).data
    
    def create(self, validated_data):
        # здесь логика создания нового меню айтема и связывание продуктов с этим меню айтемом хз правильно ли сделал если че потом починим
        menu_products_data = validated_data.pop('menu_products')
        menu = Menu.objects.create(**validated_data)
        for product_data in menu_products_data:
            MenuProducts.objects.create(menu=menu, **product_data)
        return menu
