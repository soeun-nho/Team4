from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import viewsets,  permissions
from .models import *
from .serializers import *
from rest_framework import permissions
from rest_framework.views import APIView

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.writer == request.user

class IsCommentAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow GET, HEAD, or OPTIONS requests without checking further
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow the author of the comment to edit or delete it
        return obj.user == request.user

class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all().order_by('-id')
    serializer_class = DeliverySerializer
    permission_classes = [IsOwnerOrReadOnly] 

    #글작성
    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)
    
    #상태변경
    @action(detail=True, methods=['PATCH'], permission_classes=[IsOwnerOrReadOnly])
    def confirm_purchase(self, request, pk=None):
        try:
            delivery = self.get_object()
        except Delivery.DoesNotExist:
            return Response({'error': '게시글을 찾을 수 없음.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user == delivery.writer:
            delivery.is_completed = True  # 구매 확정을 True로 설정
            delivery.save()
            return Response({'status': '구매가 확정되었습니다.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': '권한이 없습니다.(작성자가 아님)'}, status=status.HTTP_403_FORBIDDEN)
        
    #삭제 
    def destroy(self, request, *args, **kwargs):
        try:
            delivery = self.get_object()
        except Delivery.DoesNotExist:
            return Response({'error': '게시글을 찾을 수 없음.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user == delivery.writer:
            delivery.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': '권한이 없습니다.(작성자가 아님)'}, status=status.HTTP_403_FORBIDDEN)
        

class DeliveryCommentViewSet(viewsets.ModelViewSet):
    queryset = DeliveryComment.objects.all()
    serializer_class = DeliveryCommentSerializer
    permission_classes = [IsCommentAuthorOrReadOnly]

    def perform_create(self, serializer):
        delivery_id = self.kwargs['id']  # 이 부분에서 URL에서 delivery_id를 가져옵니다.
        delivery = Delivery.objects.get(id=delivery_id)
        serializer.save(post=delivery, user=self.request.user)
    
    # create 메서드 추가
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    

class GroceryViewSet(viewsets.ModelViewSet):
    queryset = Grocery.objects.all().order_by('-id') # 최근글이 앞으로 오도록 정렬(default)
    serializer_class = GrocerySerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    #상태변경
    @action(detail=True, methods=['PATCH'], permission_classes=[IsOwnerOrReadOnly])
    def confirm_purchase(self, request, pk=None):
        try:
            grocery = self.get_object()
        except Grocery.DoesNotExist:
            return Response({'error': '게시글을 찾을 수 없음.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user == grocery.writer:
            grocery.is_completed = True  # 구매 확정을 True로 설정
            grocery.save()
            return Response({'status': '구매가 확정되었습니다.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': '권한이 없습니다.(작성자가 아님)'}, status=status.HTTP_403_FORBIDDEN)
        
    #삭제 
    def destroy(self, request, *args, **kwargs):
        try:
            grocery = self.get_object()
        except Grocery.DoesNotExist:
            return Response({'error': '게시글을 찾을 수 없음.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user == grocery.writer:
            grocery.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': '권한이 없습니다.(작성자가 아님)'}, status=status.HTTP_403_FORBIDDEN)
        

# class GroceryCommentViewSet(viewsets.ModelViewSet):
#     queryset = GroceryComment.objects.all()
#     serializer_class = GroceryCommentSerializer
#     permission_classes = [IsCommentAuthorOrReadOnly]

#     def perform_create(self, serializer):
#         delivery_id = self.kwargs['id']  # 이 부분에서 URL에서 delivery_id를 가져옵니다.
#         delivery = Delivery.objects.get(id=delivery_id)
#         serializer.save(post=delivery, user=self.request.user)
    
#     # create 메서드 추가
#     def create(self, request, *args, **kwargs):
#         return super().create(request, *args, **kwargs)


class GroceryCommentView(APIView):   # 댓글 리스트
    permission_classes = [IsCommentAuthorOrReadOnly]

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
    permission_classes = [IsCommentAuthorOrReadOnly]
    
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