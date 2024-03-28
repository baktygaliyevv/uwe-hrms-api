from rest_framework import generics
from ...models import Tables
from .serializers import TableSerializer
from rest_framework.response import Response

class EditDeleteTable(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tables.objects.all()
    serializer_class = TableSerializer
    lookup_field = 'id'

class GetAllTables(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        queryset = Tables.objects.all()
        serializer_class = TableSerializer(queryset, many=True)
        return Response({
            'status': 'Ok',
            'payload': serializer_class.data
        })

class AddTable(generics.CreateAPIView):
    queryset = Tables.objects.all()
    serializer_class = TableSerializer