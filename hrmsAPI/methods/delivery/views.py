from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from ...models import Deliveries
from .serializers import DeliveryReadSerializer, DeliveryCreateUpdateSerializer, DeliveryUISerializer
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

class AddUiClientDelivery(generics.CreateAPIView):
    queryset = Deliveries.objects.all()
    serializer_class = DeliveryUISerializer

    def create(self, request, *args, **kwargs):
        user_data = {
            'email': request.data.get('email'),
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            # Добавьте другие поля, если это необходимо
        }
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            delivery_data = request.data.copy()
            delivery_data['user'] = user.id
            delivery_serializer = self.get_serializer(data=delivery_data)
            if delivery_serializer.is_valid():
                delivery_serializer.save()
                return Response(delivery_serializer.data, status=status.HTTP_201_CREATED)
            else:
                # Удаляем пользователя, если не удалось создать доставку
                user.delete()
                return Response(delivery_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
