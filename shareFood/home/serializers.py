# serializers.py
from rest_framework import serializers
from .models import *

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'
    
    def get_comments(self, obj):
        comments = DeliveryComment.objects.filter(post=obj)
        serializer = DeliveryCommentSerializer(comments, many=True)
        return serializer.data


class DeliveryCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryComment
        fields = '__all__'


class GroceryCommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)
    class Meta:
        model = GroceryComment
        fields = ['id', 'post_id', 'user', 'created_at', 'content']



class GrocerySerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)
    comments = serializers.SerializerMethodField()
        
    class Meta:
        model = Grocery
        fields = '__all__'
        
    def get_comments(self, obj):
        comments = GroceryComment.objects.filter(post=obj)
        serializer = GroceryCommentSerializer(comments, many=True)
        return serializer.data
