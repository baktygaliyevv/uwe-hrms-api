from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from ...models import Deliveries, DeliveryMenu
from specializer import DeliverySerializer, DeliveryMenuSerializer

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

class AddItemToDelivery():
    queryset = DeliveryMenu.objects.all()
    serializer_class = DeliveryMenuSerializer
    # если что я не знал что тут точно написать, поэтому неуверен(перформ написал чат)
    def perform_create(self, serializer):
        delivery_id = self.kwargs.get('delivery_id')
        delivery = generics.get_object_or_404(Deliveries, id=delivery_id)
        serializer.save(delivery=delivery)
class EditItemQuantity(generics.UpdateAPIView):
    queryset = DeliveryMenu.objects.all()
    serializer_class = DeliveryMenuSerializer
    lookupfiled = 'id'
