from rest_framework import serializers
from ...models import Users, UserTokens, EmailCodes
import hashlib
import secrets
from datetime import datetime, timedelta
from django.conf import settings
import os



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'first_name', 'last_name', 'email', 'role', 'verified')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Users(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            role=validated_data.get('role', 'client'),
            verified=validated_data.get('verified', False)
        )
        password = validated_data.pop('password', None)
        if password:
            salt = secrets.token_hex(16)  # Generate a new salt
            user.salt = salt
            user.hash = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
        user.save()
        return user

class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTokens
        fields = ('token', 'expiration_date')

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ('email', 'password', 'first_name', 'last_name', 'role', 'verified')

    def create(self, validated_data):
        validated_data['salt'] = secrets.token_hex(16)
        validated_data['hash'] = hashlib.sha256(
            (validated_data.pop('password') + validated_data['salt']).encode('utf-8')
        ).hexdigest()
        validated_data['verified'] = False  
        user = Users.objects.create(**validated_data)
        
        code = secrets.token_urlsafe()
        EmailCodes.objects.create(user=user, code=code, expiration_date=datetime.now() + timedelta(days=2))
        
        send_verification_email(user.email, code)
        
        return user

def send_verification_email(to_email, code):
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail

    verification_link = f"{settings.FRONTEND_URL}/verify?code={code}"
    message = Mail(
        from_email=settings.SENDGRID_FROM_EMAIL,
        to_emails=to_email,
        subject='Verify your email',
        html_content=f'Please verify your email by clicking on this link: <a href="{verification_link}">Verify Email</a>'
    )
    
    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
