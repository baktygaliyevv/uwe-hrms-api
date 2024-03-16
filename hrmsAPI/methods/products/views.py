from rest_framework import generics
from ...models import Products
from .serializers import ProductSerializer

class GetProducts(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

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
