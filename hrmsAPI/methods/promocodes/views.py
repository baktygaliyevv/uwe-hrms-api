from rest_framework import generics
from ...models import Promocodes
from .serializers import PromocodeSerializer
from rest_framework.response import Response

class GetAllPromocodes(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        queryset = Promocodes.objects.all()
        serializer_class = PromocodeSerializer(queryset, many=True)
        return Response({
            'status': 'Ok',
            'payload': serializer_class.data
        })

class AddPromocode(generics.CreateAPIView):
    queryset = Promocodes.objects.all()
    serializer_class = PromocodeSerializer

class DeletePromocode(generics.DestroyAPIView):
    queryset = Promocodes.objects.all()
    serializer_class = PromocodeSerializer
    lookup_field = 'id'

class GetSpecificPromocode(generics.RetrieveAPIView):
    queryset = Promocodes.objects.all()
    serializer_class = PromocodeSerializer  # Just a reference to the class
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        promocode = self.get_object()
        serializer = self.get_serializer(promocode)
        return Response({
            'status': 'Ok',
            'payload': serializer.data 
        })
