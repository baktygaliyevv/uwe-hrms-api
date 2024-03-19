from rest_framework import serializers
from ...models import Tables

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tables
        fields = ('id', 'restaurant', 'capacity')