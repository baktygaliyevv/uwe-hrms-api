from rest_framework import generics
from ...models import Tables
from .serializers import TableSerializer

class GetAddTable(generics.ListCreateAPIView):
    queryset = Tables.objects.all()
    serializer_class = TableSerializer

class EditDeleteTable(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tables.objects.all()
    serializer_class = TableSerializer
    lookup_field = 'id'
