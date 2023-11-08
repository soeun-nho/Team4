from django.core import serializers
from rest_framework import serializers
from .models import GroceryComment, Grocery, Delivery


class GroceryCommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)
    class Meta:
        model = GroceryComment
        fields = ['id', 'post', 'user', 'created_at', 'content']



class GrocerySerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)
    comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Grocery
        fields = ['id', 'user', 'title', 'content', 'unit', 'location',
                'price', 'created_at', 'image', 'buy_time','recruitment_num',
                'post_type', 'is_completed', 'comments']
        
    def get_comments(self, obj):
        comments = GroceryComment.objects.filter(post=obj)
        serializer = GroceryCommentSerializer(comments, many=True)
        return serializer.data
