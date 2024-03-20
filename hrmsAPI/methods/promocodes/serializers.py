from rest_framework import serializers
from ...models import Promocodes

class PromocodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promocodes
        fields = ['id', 'discount', 'valid_till']
