from rest_framework import generics
from rest_framework.response import Response
from ...models import Products
from .serializers import ProductSerializer

class GetProducts(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        queryset = Products.objects.all()
        serializer_class = ProductSerializer(queryset, many=True)
        for product in serializer_class.data:
            product['vegan'] = bool(product['vegan'])
            product['vegetarian'] = bool(product['vegetarian'])
            product['gluten_free'] = bool(product['gluten_free'])
        return Response({
            'status': 'Ok',
            'payload': serializer_class.data
        })
    
class AddProduct(generics.CreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

class EditProduct(generics.UpdateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

class DeleteProduct(generics.DestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
