from rest_framework import generics
from ...models import RestaurantProducts
from .serializers import RestaurantProductsSerializer
from rest_framework.response import Response

class GetRetaurantProducts(generics.ListAPIView):
    
    def list(self, request, *args, **kwargs):
        queryset = RestaurantProducts.objects.all()
        serializer_class = RestaurantProductsSerializer(queryset,many = True)
        return Response({
            'status' : 'Ok',
           'payload' : serializer_class.data
            })