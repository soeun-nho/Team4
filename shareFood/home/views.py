from django.shortcuts import render, get_object_or_404
from .models import GroceryComment, Grocery, Delivery
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import GrocerySerializer, GroceryCommentSerializer, GroceryDetailSerializer


# Create your views here.


class GroceryView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        post = Grocery.objects.all()
        serializer = GrocerySerializer(post, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = GrocerySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

class GroceryDetailView(APIView):   # 게시글 상세
    authentication_classes = [JWTAuthentication]

    def get(self, request, post_id):
        post = get_object_or_404(Grocery, pk=post_id)
        serializer = GroceryDetailSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, post_id):
        post = get_object_or_404(Grocery, pk=post_id)
        serializer = GrocerySerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        post = get_object_or_404(Grocery, pk=post_id)
        post.delete()
        return Response({'message': '삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)


class GroceryCommentView(APIView):   # 댓글 리스트
    authentication_classes = [JWTAuthentication]

    def get(self, request, post_id):
        comment = GroceryComment.objects.filter(post=post_id)
        serializer = GroceryCommentSerializer(comment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, post_id):
        serializer = GroceryCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post_id=post_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

class GroceryCommentDetailView(APIView):   # 댓글 상세
    authentication_classes = [JWTAuthentication]
    
    def patch(self, request, post_id, comment_id):
        comment = get_object_or_404(GroceryComment, pk=comment_id)
        serializer = GroceryCommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user, post_id=post_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, post_id, comment_id):
        comment = get_object_or_404(GroceryComment, pk=comment_id)
        comment.delete()
        return Response({'message': '삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)