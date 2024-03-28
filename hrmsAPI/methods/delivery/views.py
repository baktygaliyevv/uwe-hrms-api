from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from ...models import Deliveries
from .serializers import DeliveryReadSerializer, DeliveryCreateUpdateSerializer
from rest_framework.mixins import RetrieveModelMixin

class GetDeliveries(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        queryset = Deliveries.objects.all()
        serializer_class = DeliveryReadSerializer(queryset, many=True)
        return Response({
            'status': 'Ok',
            'payload': serializer_class.data
        })

class AddDelivery(generics.CreateAPIView):
    queryset = Deliveries.objects.all()
    serializer_class = DeliveryCreateUpdateSerializer

class EditDelivery(RetrieveModelMixin, generics.UpdateAPIView):
    queryset = Deliveries.objects.all()
    serializer_class = DeliveryCreateUpdateSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class DeleteDelivery(generics.DestroyAPIView):
    queryset = Deliveries.objects.all()
    serializer_class = DeliveryCreateUpdateSerializer
    lookup_field = 'id'
