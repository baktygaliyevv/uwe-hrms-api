from rest_framework import generics
from rest_framework.response import Response
from ...models import Products
from .serializers import ProductSerializer

class GetAddProducts(generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        queryset = Products.objects.all()
        serializer_class = ProductSerializer(queryset, many=True)
        return Response({
            'status': 'Ok',
            'payload': serializer_class.data
        })
    
    def create(self, request, *args, **kwargs):
        request.data['vegan'] = int(request.data['vegan'])
        request.data['vegetarian'] = int(request.data['vegetarian'])
        request.data['gluten_free'] = int(request.data['gluten_free'])
        return super().create(request, *args, **kwargs)
    

class EditProduct(generics.UpdateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

class DeleteProduct(generics.DestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
