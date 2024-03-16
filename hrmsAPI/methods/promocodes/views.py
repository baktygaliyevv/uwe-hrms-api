from rest_framework import generics
from ...models import Promocodes
from .serializers import PromocodeSerializer

class GetAllPromocodes(generics.ListAPIView):
    queryset = Promocodes.objects.all()
    serializer_class = PromocodeSerializer

class AddPromocode(generics.CreateAPIView):
    queryset = Promocodes.objects.all()
    serializer_class = PromocodeSerializer

class DeletePromocode(generics.DestroyAPIView):
    queryset = Promocodes.objects.all()
    serializer_class = PromocodeSerializer
    lookup_field = 'id'
