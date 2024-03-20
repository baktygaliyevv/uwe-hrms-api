from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from rest_framework import status
from ...models import Users, UserTokens
from .serializers import UserSerializer, UserTokenSerializer
import secrets
from datetime import timedelta, datetime

class LoginView(APIView):
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
        expiration_date = datetime.now() + timedelta(days=expiration_duration)

        UserTokens.objects.create(user=user, token=token, expiration_date=expiration_date)

        response_data = {
            "user": UserSerializer(user).data,
        }
        response = HttpResponse(JSONRenderer().render(response_data))
        response.set_cookie(key="token", value=token, expires=expiration_date, httponly=True, secure=True)
        
        return response

class SignupView(APIView):
    ### signup
    pass