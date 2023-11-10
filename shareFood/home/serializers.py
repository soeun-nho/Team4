# serializers.py
from rest_framework import serializers
from .models import *

class DeliverySerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)
    like_cnt = serializers.IntegerField(source='delivery_like.count', read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Delivery
        fields = ['id', 'user', 'title', 'content', 'location',
                'minimumPrice', 'created_at', 'image', 'link',
                'is_completed', 'comments', 'like_cnt', 'is_liked']
    
    def get_comments(self, obj):
        comments = DeliveryComment.objects.filter(post=obj)
        serializer = DeliveryCommentSerializer(comments, many=True)
        return serializer.data


class DeliveryCommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)
    class Meta:
        model = DeliveryComment
        fields = ['id', 'post_id', 'user', 'created_at', 'content']


class GroceryCommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)
    class Meta:
        model = GroceryComment
        fields = ['id', 'post_id', 'user', 'created_at', 'content']



class GrocerySerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)
    comments = serializers.SerializerMethodField()
    like_cnt = serializers.IntegerField(source='grocery_like.count', read_only=True)
        
    class Meta:
        model = Grocery
        fields = ['id', 'user', 'title', 'content', 'unit', 'location',
                'price', 'created_at', 'image', 'buy_time','recruitment_num',
                'post_type', 'is_completed', 'comments', 'like_cnt', 'is_liked']
        
    def get_comments(self, obj):
        comments = GroceryComment.objects.filter(post=obj)
        serializer = GroceryCommentSerializer(comments, many=True)
        return serializer.data




class GroceryLikeSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = GroceryLike
        fields = '__all__'

    def create(self, validated_data):
        post = validated_data['post']
        user = validated_data['user']
        grocery_like, created = GroceryLike.objects.get_or_create(post=post, user=user)

        # 좋아요를 생성하거나 삭제할 때, Grocery 모델의 like_cnt 업데이트
        post.like_cnt = GroceryLike.objects.filter(post=post).count()
        post.save()

        if not created:
            grocery_like.delete()
            # 좋아요 한 번 더 누르면 like_cnt를 1 감소
            post.like_cnt -= 1
            post.save()
        
        return grocery_like


class DeliveryLikeSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = DeliveryLike
        fields = '__all__'

    def create(self, validated_data):
        post = validated_data['post']
        user = validated_data['user']
        delivery_like, created = DeliveryLike.objects.get_or_create(post=post, user=user)

        # 좋아요를 생성하거나 삭제할 때, Grocery 모델의 like_cnt 업데이트
        post.like_cnt = DeliveryLike.objects.filter(post=post).count()
        post.save()

        if not created:
            delivery_like.delete()
            # 좋아요 한 번 더 누르면 like_cnt를 1 감소
            post.like_cnt -= 1
            post.save()
        
        return delivery_like
    

class DeliveryApplicationSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = DeliveryApplication
        fields = '__all__'

class GroceryApplicationSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = GroceryApplication
        fields = '__all__'