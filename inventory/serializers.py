from rest_framework import serializers
from .models import *


class Scans_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Scans
        fields = '__all__'


class UpcDetail_Serializer(serializers.ModelSerializer):
    class Meta:
        model = UpcDetail
        fields = '__all__'

class OnHand_Serializer(serializers.ModelSerializer):
    onhand = serializers.IntegerField()

    class Meta:
        model = UpcDetail
        fields = ('id', 'description', 'details', 'image', 'category', 'grams', 'onhand')