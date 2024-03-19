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
