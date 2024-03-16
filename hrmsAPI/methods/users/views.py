from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserSerializer
from ...models import Users

class GetAllUsers(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

class AddUser(generics.CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)