import hashlib
import secrets
from rest_framework import serializers
from ...models import Users

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'role')

    def create(self, validated_data):
        password = validated_data.pop('password')
        salt = secrets.token_hex(16)
        hashed_password = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

        user = Users.objects.create(
            salt=salt,
            hash=hashed_password,
            verified=1,
            **validated_data
        )
        
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            salt = secrets.token_hex(16)
            instance.hash = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
            instance.salt = salt

        return super(UserSerializer, self).update(instance, validated_data)