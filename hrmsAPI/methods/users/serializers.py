# from rest_framework import serializers
# from ...models import Users

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Users
#         fields = ['id', 'first_name', 'last_name', 'email', 'role', 'verified']
#         extra_kwargs = {
#             'hash': {'write_only': True},
#             'salt': {'write_only': True}           
#         }

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from ...models import Users

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Users
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'role', 'verified')
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        hashed_password = make_password(password)
        validated_data['hash'] = hashed_password
        user = Users.objects.create(**validated_data)
        
        return user

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        if password:
            instance.hash = make_password(password)
        return super(UserSerializer, self).update(instance, validated_data)

# надо вместе обсудить и подумать как сделать добавления юзера, потому что в джанго из коробки есть тема чтобы сохранять пароли безопасно, я потестил и вот хз норм или нет