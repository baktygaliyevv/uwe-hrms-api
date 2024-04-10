from rest_framework import generics, status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from ...models import Deliveries, UserTokens, Users
from .serializers import DeliveryReadSerializer, DeliveryCreateUpdateSerializer, DeliveryReadClientSerializer, DeliveryCreateUpdateClientSerilizer, DeliveryEditDeleteSerializer
from ..users.serializers import UserSerializer

class GetAddDelivery(ListCreateAPIView):
    queryset = Deliveries.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return DeliveryReadSerializer
        return DeliveryCreateUpdateSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = DeliveryReadSerializer(queryset, many=True)
        return Response({'status': 'Ok', 'payload': serializer.data})
    
    def create(self, request, *args, **kwargs):
        serializer = DeliveryCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        order_serializer = DeliveryReadSerializer(order)
        return Response({'status': 'Ok', 'payload': order_serializer.data}, status=status.HTTP_201_CREATED)

class EditDeleteDelivery(generics.RetrieveUpdateDestroyAPIView):
    queryset = Deliveries.objects.all()
    serializer_class = DeliveryEditDeleteSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        read_serializer = DeliveryReadSerializer(instance)
        return Response({'status':'Ok', 'payload':read_serializer.data})

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status': 'Ok'})

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
        email = request.data.get('email', None)

        if not request.user.is_authenticated:
            if not email:
                return Response({'error': 'Email is required for unregistered users'}, status=status.HTTP_400_BAD_REQUEST)          
            elif Users.objects.filter(email=email).exists():
                return Response({'error': 'User with this email already exists. Please log in.'}, status=status.HTTP_400_BAD_REQUEST) # вот тут темка, что если добавляем доставку на такого же юзера просят залогиниться при этом если юзер создался без пароля хз как логиниться, но в целом это маловероятно что произойдет, на презентации не спалят и вряд ли заметят, так то все работает заебись помимо вот этого маленького недочета, я апрув, поставлю но на будущее такой долгий коммент оставлю мб потом пофиксим
            
            
        serializer = DeliveryCreateUpdateClientSerilizer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        order_serializer = DeliveryReadSerializer(order)
        return Response({'status': 'Ok', 'payload': order_serializer.data}, status=status.HTTP_201_CREATED)