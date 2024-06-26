from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
from ...models import Menu, MenuProducts, MenuCategories, RestaurantProducts
from .serializers import AvailableMenuSerializer, MenuSerializer, MenuProductSerializer, MenuCategorySerializer, UnavailableMenuSerializer, MenuAddSerializer

class GetAddMenuItems(generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'list':
            return MenuSerializer
        return MenuAddSerializer

    def get(self, request, *args, **kwargs):
        queryset = Menu.objects.all()
        serializer_class = MenuSerializer(queryset, many=True)
        return Response({
            'status': 'Ok',
            'payload': serializer_class.data
        })
    
    def create(self, request, *args, **kwargs):
        serializer = MenuAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        menu_serializer = MenuSerializer(serializer.save())
        return Response({'status': 'Ok', 'payload': menu_serializer.data})
    

class EditDeleteMenuItem(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    lookup_field = 'id'

    def perform_destroy(self, instance):
        MenuProducts.objects.filter(menu=instance).delete()
        instance.delete()

class AddMenuProduct(APIView):
    def post(self, request, id):
        menu = generics.get_object_or_404(Menu, id=id)
        serializer = MenuProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(menu=menu)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteMenuProduct(APIView):
    serializer_class = MenuProductSerializer
    
    def delete(self, request, id, productId):
        with connection.cursor() as cursor:
            query = """DELETE FROM menu_products WHERE menu_id = %s AND product_id = %s"""
            cursor.execute(query, [id, productId])
        return Response({'status':"Ok"})

class GetAddMenuCategories(generics.ListCreateAPIView):
    queryset = MenuCategories.objects.all()
    serializer_class = MenuCategorySerializer

    def get(self, request, *args, **kwargs):
        queryset = MenuCategories.objects.all()
        serializer_class = MenuCategorySerializer(queryset, many=True)
        return Response({
            'status': 'Ok',
            'payload': serializer_class.data
        })

@api_view(['GET'])
def available_menu_items(request):
    restaurant_id = request.query_params.get('restaurant_id')
    if not restaurant_id:
        return Response({'error': 'restaurant_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        restaurant_products = RestaurantProducts.objects.filter(restaurant_id=restaurant_id).values_list('product_id', flat=True)
        menu_items = MenuProducts.objects.filter(product_id__in=restaurant_products).values_list('menu_id', flat=True).distinct()
        available_menus = Menu.objects.filter(id__in=menu_items)
        serializer = AvailableMenuSerializer(available_menus, many=True)
        
        return Response({'status': 'OK', 'payload': serializer.data})
    except Exception as e:
        return Response({'status': 'Error', 'message': str(e)})

@api_view(['GET'])
def unavailable_menu_items(request):
    restaurant_id = request.query_params.get('restaurant_id')
    if not restaurant_id:
        return Response({'error': 'restaurant_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        restaurant_products_ids = RestaurantProducts.objects.filter(restaurant_id=restaurant_id).values_list('product_id', flat=True)
        available_menu_ids = MenuProducts.objects.filter(product_id__in=restaurant_products_ids).values_list('menu_id', flat=True).distinct()
        unavailable_menus = Menu.objects.exclude(id__in=available_menu_ids)
        serializer = UnavailableMenuSerializer(unavailable_menus, many=True)

        return Response({'status': 'OK', 'payload': serializer.data})
    except Exception as e:
        return Response({'status': 'Error', 'message': str(e)})