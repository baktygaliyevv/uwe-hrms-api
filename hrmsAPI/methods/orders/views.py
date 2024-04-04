from rest_framework import generics, status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from ...models import Orders, OrderMenu, Menu, UserTokens
from .serializers import OrderGetSerializer, OrderMenuAddSerializer, OrderAddSerializer, MenuSerializer, OrderAddClientSerializer, OrderMenuEditDeleteSerializer, MultipleFieldLookupMixin, OrderEditDeleteSerializer, OrderGetClientSerializer, UserSerializer

class GetAddOrder(ListCreateAPIView):
    queryset = Orders.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return OrderGetSerializer
        return OrderAddSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = OrderGetSerializer(queryset, many=True)
        return Response({'status': 'Ok', 'payload': serializer.data})
    
    def create(self, request, *args, **kwargs):
        serializer = OrderAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        order_serializer = OrderGetSerializer(order)
        return Response({'status': 'Ok', 'payload': order_serializer.data}, status=status.HTTP_201_CREATED)

class GetAddClientOrder(ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'list':
            return OrderGetClientSerializer
        return OrderAddClientSerializer
    
    def list(self, request):
        obj = UserTokens.objects.get(token=request.COOKIES['token'])
        user_id = UserSerializer(obj.user).data.get('id')
        queryset = Orders.objects.filter(user_id = user_id)
        serializer_class = OrderGetClientSerializer(queryset, many=True)
        return Response({
            'status': 'Ok',
            'payload': serializer_class.data
        })
    
    def create(self, request, *args, **kwargs):
            serializer = OrderAddClientSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            order = serializer.save()
            order_serializer = OrderGetSerializer(order)
            return Response({'status': 'Ok', 'payload': order_serializer.data}, status=status.HTTP_201_CREATED)

class EditDeleteOrder(generics.RetrieveUpdateDestroyAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrderEditDeleteSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'status':'Ok', 'payload':serializer.data})

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status': 'Ok'})

class EditDeleteOrderMenu(MultipleFieldLookupMixin,generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderMenu.objects.all()
    serializer_class = OrderMenuEditDeleteSerializer
    lookup_fields = ('order_id','menu_id')

    def update(self,request,*args,**kwargs):
        item_id = self.kwargs.get('menu_id')
        order_id = self.kwargs.get('order_id')
        item = OrderMenu.objects.get(order_id=order_id, menu_id=item_id)
        serializer = self.get_serializer(instance=item, data=request.data)
        if serializer.is_valid():
            serializer.save(order_id = order_id,menu_id = item_id)
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

class AddOrderMenu(generics.CreateAPIView):
    serializer_class = OrderMenuAddSerializer
    queryset = OrderMenu.objects.all()

    def create(self, request, *args, **kwargs):
        order_id = self.kwargs.get('order_id')
        data = request.data.copy()
        data['menu'] = data.pop('item_id')
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            serializer.save(order=order_id)
            item = Menu.objects.get(pk=serializer.validated_data['menu'])
            item_serializer = MenuSerializer(item)
            return_data = {
                'item': item_serializer.data,
                'quantity': serializer.validated_data['quantity']
            }
            return Response({
                'status': 'Ok',
                'payload': return_data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)