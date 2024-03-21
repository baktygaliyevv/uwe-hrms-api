from rest_framework import generics
from rest_framework.response import Response
from ...models import Orders
from .serializers import OrderSerializer

class GetOrder(generics.ListCreateAPIView):
    serializer_class=OrderSerializer
    def get(self, request, *args, **kwargs):
        queryset = Orders.objects.all()
        serializer_class = OrderSerializer(queryset, many=True)
        return Response({
            'status': 'Ok',
            'payload': serializer_class.data
        })

class AddOrder(generics.CreateAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer

class EditDeleteOrder(generics.RetrieveUpdateDestroyAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'id'