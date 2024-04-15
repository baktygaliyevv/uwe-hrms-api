from rest_framework import generics
from rest_framework.response import Response
from ...models import Products
from .serializers import ProductSerializer

class GetAddProducts(generics.ListCreateAPIView):
    serializer_class = ProductSerializer

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
    
    def create(self, request, *args, **kwargs):
        request.data['vegan'] = int(request.data['vegan'])
        request.data['vegetarian'] = int(request.data['vegetarian'])
        request.data['gluten_free'] = int(request.data['gluten_free'])
        return Response({
            'status': 'Ok',
            'payload': super().create(request, *args, **kwargs).data
        })
    
class EditDeleteProduct(generics.RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        for field in ['vegan', 'vegetarian', 'gluten_free']:
            if field in request.data:
                request.data[field] = int(request.data[field] == 'true' or request.data[field] == True)

        return super().update(request, *args, **kwargs)