from rest_framework import generics, status
from rest_framework.response import Response
from ...models import Bookings, UserTokens
from .serializers import BookingSerializer, ClientBookingSerializer
from django.utils import timezone

class GetAddBookings(generics.GenericAPIView):
    queryset = Bookings.objects.all()
    serializer_class = BookingSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status': 'Ok',
            'payload': serializer.data
        })

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'Ok',
                'payload': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'Error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class EditBooking(generics.UpdateAPIView):
    queryset = Bookings.objects.all()
    serializer_class = BookingSerializer
    lookup_field = 'id'

class DeleteBooking(generics.DestroyAPIView):
    queryset = Bookings.objects.all()
    serializer_class = BookingSerializer
    lookup_field = 'id'

class ClientGetAddBookings(generics.ListCreateAPIView):
    serializer_class = ClientBookingSerializer

    def get_queryset(self):
        user_token = self.request.COOKIES.get('token')
        user_tokens = UserTokens.objects.filter(token=user_token, expiration_date__gt=timezone.now())
        if user_tokens.exists():
            return Bookings.objects.filter(user=user_tokens.first().user)
        return Bookings.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status': 'Ok',
            'payload': serializer.data
        })
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()
        return Response({
            'status': 'Ok',
            'payload': BookingSerializer(booking, context={'request': request}).data
        }, status=status.HTTP_201_CREATED)