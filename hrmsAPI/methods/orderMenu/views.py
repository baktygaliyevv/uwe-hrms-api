from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from .serializers import OrderMenuSerializer
from ...models import OrderMenu



class EditOrderMenu(generics.UpdateAPIView):
    queryset = OrderMenu.objects.all()
    serializer_class = OrderMenuSerializer
    lookup_field = 'order_id'

class AddOrderMenu(APIView):
    def post(self, request, order_id):
        order_menu = generics.get_object_or_404(OrderMenu, order_id=order_id)
        serializer = OrderMenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(order_menu=order_menu)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteOrderMenu(APIView):
    def delete(self, request, order_id):
        order_menu = generics.get_object_or_404(OrderMenu,order_id=order_id)
        order_menu.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)