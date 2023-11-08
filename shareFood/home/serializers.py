# serializers.py
from rest_framework import serializers
from .models import Delivery,DeliveryComment

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'

class DeliveryCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryComment
        fields = '__all__'