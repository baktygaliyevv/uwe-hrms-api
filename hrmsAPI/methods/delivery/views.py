from rest_framework import generics, status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from ...models import Deliveries, UserTokens, Users, DeliveryMenu, Menu
from .serializers import DeliveryReadSerializer, DeliveryCreateUpdateSerializer, DeliveryReadClientSerializer, DeliveryCreateUpdateClientSerilizer, DeliveryEditDeleteSerializer, MultipleFieldLookupMixin, DeliveryMenuEditDeleteSerializer, DeliveryMenuAddSerializer, DeliveryMenuSerializer, MenuSerializer
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
        delivery = serializer.save()
        delivery_serializer = DeliveryReadSerializer(delivery)
        return Response({'status': 'Ok', 'payload': delivery_serializer.data}, status=status.HTTP_201_CREATED)

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
        serializer = DeliveryCreateUpdateClientSerilizer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        delivery = serializer.save()
        if isinstance(delivery,Response):
                return Response({ "status": "Error", "payload": "Unauthorized" }, status=status.HTTP_400_BAD_REQUEST)
        delivery_serializer = DeliveryReadSerializer(delivery)
        return Response({'status': 'Ok', 'payload': delivery_serializer.data})
    
class EditDeleteDeliveryMenu(MultipleFieldLookupMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = DeliveryMenu.objects.all()
    serializer_class = DeliveryMenuEditDeleteSerializer
    lookup_fields = ('delivery_id','menu_id')

    def update(self,request,*args,**kwargs):
        item_id = self.kwargs.get('menu_id')
        delivery_id = self.kwargs.get('delivery_id')
        item = DeliveryMenu.objects.get(delivery_id=delivery_id, menu_id=item_id)
        serializer = self.get_serializer(instance=item, data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save(delivery_id = delivery_id,menu_id = item_id)
        menu = Menu.objects.get(pk=item_id)
        item_serializer = MenuSerializer(menu)
        return_data = {
            'item': item_serializer.data,
            'quantity': serializer.validated_data.get('quantity')
        }
        return Response({
            'status':'Ok', 
            'payload': return_data
        })
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status': 'Ok'})
    

class AddDeliveryMenu(generics.CreateAPIView):
    serializer_class = DeliveryMenuAddSerializer
    queryset = DeliveryMenu.objects.all()

    def create(self, request, *args, **kwargs):
        delivery_id = self.kwargs.get('delivery_id')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        serializer.validated_data['menu_id'] = serializer.validated_data.pop('item_id')
        serializer.save(delivery_id = delivery_id)
        menu_id = serializer.validated_data.get('menu_id')
        menu = Menu.objects.get(pk=menu_id)
        item_serializer = MenuSerializer(menu)
        return_data = {
            'item': item_serializer.data,
            'quantity': serializer.validated_data.get('quantity')
        }
        return Response({
            'status':'Ok', 
            'payload': return_data
        })
