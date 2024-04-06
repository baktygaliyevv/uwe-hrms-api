from rest_framework import generics
from ...models import RestaurantProducts
from .serializers import RestaurantProductsSerializer, RestaurantProductIncDecSerializer
from rest_framework.response import Response

class GetRetaurantProducts(generics.ListAPIView):
    
    def list(self, request, *args, **kwargs):
        queryset = RestaurantProducts.objects.all()
        serializer_class = RestaurantProductsSerializer(queryset,many = True)
        return Response({
            'status' : 'Ok',
            'payload' : serializer_class.data
            })
    
class IncRestaurntProducts(generics.UpdateAPIView):
    serializer_class = RestaurantProductIncDecSerializer

    def update(self, request, *args, **kwargs):
        try:
            instance = RestaurantProducts.objects.get(restaurant_id = request.data.get('restaurant_id'),product_id = request.data.get('product_id'))
            instance.count += 1
            instance.save()
        except:
            instance = RestaurantProducts.objects.create(count=1, **request.data)
        return Response({
            'status' : 'Ok',
            'payload' : RestaurantProductsSerializer(RestaurantProducts.objects.get(restaurant_id = request.data.get('restaurant_id'),product_id = request.data.get('product_id'))).data
            })