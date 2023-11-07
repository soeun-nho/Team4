from django.core import serializers
from rest_framework import serializers
from .models import GroceryComment, Grocery, Delivery


class GrocerySerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)
    class Meta:
        model = Grocery
        fields = ['id', 'user', 'title', 'content', 'unit', 'location',
                'price', 'created_at', 'image', 'buy_time','recruitment_num',
                'post_type', 'is_completed']


class GroceryCommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)
    class Meta:
        model = GroceryComment
        fields = ['id', 'post_id', 'user', 'created_at', 'content']


class GroceryDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)
    comments = GroceryCommentSerializer(many=True, read_only=True, source='comment_set')
    class Meta:
        model = Grocery
        fields = ['id', 'user', 'title', 'content', 'unit', 'location',
                'price', 'created_at', 'image', 'buy_time','recruitment_num',
                'post_type', 'is_completed', 'comments']