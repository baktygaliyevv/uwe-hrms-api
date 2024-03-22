from rest_framework import generics
from rest_framework.response import Response
from ...models import Restaurants
from .serializers import RestaurantSerializer

class GetRestaurant(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        queryset = Restaurants.objects.all()
        serializer_class = RestaurantSerializer(queryset, many=True)
        return Response({
            'status': 'Ok',
            'payload': serializer_class.data
        })

class DeleteRestaurant(generics.DestroyAPIView):
    queryset = Restaurants.objects.all()
    serializer_class = RestaurantSerializer
    lookup_field = 'id'