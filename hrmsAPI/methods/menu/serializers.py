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
    product_id = serializers.PrimaryKeyRelatedField(queryset=Products.objects.all(), source='product', write_only=True)

    class Meta:
        model = MenuProducts
        fields = ['product', 'product_id']

class MenuSerializer(serializers.ModelSerializer):
    category = MenuCategorySerializer(read_only=True, source='menu_category')
    products = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ['id', 'name', 'category', 'price', 'products']

    def get_products(self, obj):
        menu_products = MenuProducts.objects.filter(menu=obj)
        product_ids = menu_products.values_list('product', flat=True)
        products = Products.objects.filter(id__in=product_ids)
        return ProductSerializer(products, many=True).data
    
    
    def update(self, instance, validated_data):
        if 'menu_category' in validated_data:
            instance.menu_category = validated_data.pop('menu_category')
        return super(MenuSerializer, self).update(instance, validated_data)
    
class MenuAddSerializer(serializers.ModelSerializer):

    name = serializers.CharField(required=True)
    products = serializers.ListField(required=True)
    category_id = serializers.IntegerField(required=True)
    price = serializers.IntegerField(required=True)

    class Meta:
        model = Menu
        fields = ['name', 'category_id','price', 'products'] 
    
    def create(self, validated_data):
        products_ids = validated_data.pop('products')
        validated_data['menu_category_id'] = validated_data.pop('category_id')
        menu = Menu.objects.create(**validated_data)
        for product_id in list(products_ids):
            product_instance = Products.objects.get(id=product_id)
            MenuProducts.objects.create(menu=menu, product=product_instance)
        return menu

class AvailableMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class UnavailableMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'