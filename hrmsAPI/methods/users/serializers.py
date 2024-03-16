from rest_framework import serializers
from ...models import Users

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'first_name', 'last_name', 'email', 'role', 'verified']
        extra_kwargs = {
            'hash': {'write_only': True},
            'salt': {'write_only': True}           
        }