from rest_framework import generics, status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from ...models import Deliveries, UserTokens
from .serializers import DeliveryReadSerializer, DeliveryCreateUpdateSerializer, DeliveryReadClientSerializer, DeliveryCreateUpdateClientSerilizer
from ..users.serializers import UserSerializer
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

class GetAddClientDeliveries(ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'list':
            return DeliveryReadClientSerializer
        return DeliveryCreateUpdateClientSerilizer

    def list(self, request):
        obj = UserTokens.objects.get(token=request.COOKIES['token'])
        user_id = UserSerializer(obj.user).data.get('id')
        queryset = Deliveries.objects.filter(user_id = user_id)
        serializer_class = DeliveryReadClientSerializer(queryset, many=True)
        return Response({
            'status': 'Ok',
            'payload': serializer_class.data
        })
    
    def create(self, request, *args, **kwargs):
            serializer = DeliveryCreateUpdateClientSerilizer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            order = serializer.save()
            order_serializer = DeliveryReadSerializer(order)
            return Response({'status': 'Ok', 'payload': order_serializer.data}, status=status.HTTP_201_CREATED)