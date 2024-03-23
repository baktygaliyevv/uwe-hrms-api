from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from ...models import Deliveries, DeliveryMenu
from .serializers import DeliverySerializer, DeliveryMenuSerializer

class GetAllDelivery(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        queryset = Deliveries.objects.all()
        serializer_class = DeliverySerializer(queryset, many=True)
        return Response({
            'status': 'Ok',
            'payload': serializer_class.data
        })

class AddDelivery(generics.CreateAPIView):  
    queryset = Deliveries.objects.all()
    serializer_class = DeliverySerializer

class EditDelivery(generics.UpdateAPIView):
    queryset = Deliveries.objects.all()
    serializer_class = DeliverySerializer
    lookup_field = 'id'

class DeleteDelivery(generics.DestroyAPIView):
    queryset = Deliveries.objects.all()
    serializer_class = DeliverySerializer
    lookup_field = 'id'
