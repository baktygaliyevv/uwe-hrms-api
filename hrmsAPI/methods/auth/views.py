from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from ...models import Users, UserTokens
from .serializers import UserSerializer, UserTokenSerializer, UserSignupSerializer
import secrets
from django.utils import timezone

class AuthView(APIView):
    def get(self, request, *args, **kwargs):
        # FIXME that's gonna be a middleware
        if not 'token' in request.COOKIES:
            return Response({ "status": "Error", "payload": "Unauthorized" }, status=status.HTTP_401_UNAUTHORIZED)
        try:
            obj = UserTokens.objects.get(token=request.COOKIES['token'])
            # FIXME move to utils/responses
            return Response({
                "status": "Ok",
                "payload": UserSerializer(obj.user).data
            })
        except:
            return Response({ "status": "Error", "payload": "Unauthorized" }, status=status.HTTP_401_UNAUTHORIZED)
        
    def delete(self, request, *args, **kwargs):
        token = request.COOKIES.get('token', None)
        if not token:
            return Response({"error": "No token provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_token = UserTokens.objects.get(token=token)
            user_token.delete()
            response = Response({"status": "Ok", "payload": "Logged out successfully."})
            response.delete_cookie('token')
            return response
        except UserTokens.DoesNotExist:
            return Response({"error": "Token not found."}, status=status.HTTP_404_NOT_FOUND)


class AuthLoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            return Response({"error": "Incorrect email or password."}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({"error": "Incorrect email or password."}, status=status.HTTP_401_UNAUTHORIZED)

        token = secrets.token_hex(32)
        expiration_duration = 60  # Token is valid for 60 days
        expiration_date = timezone.now() + timezone.timedelta(days=expiration_duration)

        UserTokens.objects.create(user=user, token=token, expiration_date=expiration_date)

        response_data = {
            "user": UserSerializer(user).data,
        }
        response = Response(response_data)
        response.set_cookie(key="token", value=token, expires=expiration_date, httponly=True, secure=True)
        
        return response

class AuthSignupView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Ok", "message": "User created successfully, please check your email to verify your account."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
