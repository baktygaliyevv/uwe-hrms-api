from rest_framework import serializers
from ...models import Users, UserTokens
import hashlib
import secrets
from datetime import datetime, timedelta

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'first_name', 'last_name', 'email', 'role', 'verified')
        extra_kwargs = {'hash': {'write_only': True}}

    def create(self, validated_data):
        user = Users(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            role=validated_data.get('role', 'client'),
            verified=validated_data.get('verified', False)
        )
        password = validated_data.pop('hash', None)
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
