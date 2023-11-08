from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import viewsets,  permissions
from .models import Delivery,DeliveryComment
from .serializers import DeliverySerializer,DeliveryCommentSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    글의 작성자만 수정 권한을 가짐.
    """

    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모두에게 허용.
        if request.method in permissions.SAFE_METHODS:
            return True

        # 쓰기 권한은 글의 작성자에게만 허용.
        return obj.writer == request.user
    
class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [permissions.IsAuthenticated]  # 인증된 사용자만 허용

    #글작성
    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)

    #댓글 조회
    @action(detail=True, methods=['GET'])
    def comments(self, request, pk=None):
        delivery = self.get_object()
        comments = DeliveryComment.objects.filter(post=delivery)
        serializer = DeliveryCommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    # @action(detail=True, methods=['PATCH'], permission_classes=[IsOwnerOrReadOnly])
    # def confirm_purchase(self, request, id=None):
    #     # 'delivery_id'를 URL에서 가져와서 delivery_id 변수에 할당
    #     delivery_id = int(id)

    #     # 'delivery_id'를 사용하여 해당 게시글을 가져옴
    #     try:
    #         delivery = Delivery.objects.get(pk=id)
    #     except Delivery.DoesNotExist:
    #         return Response({'error': '게시글을 찾을 수 없음.'}, status=status.HTTP_404_NOT_FOUND)

    #     if request.user == delivery.writer:
    #         # 게시글을 수정하고 저장
    #         delivery.is_completed = True  # 구매 확정을 True로 설정
    #         delivery.save()

    #         return Response({'status': '구매가 확정되었습니다.'}, status=status.HTTP_200_OK)
    #     else:
    #         return Response({'error': '권한이 없습니다.(작성자가 아님)'}, status=status.HTTP_403_FORBIDDEN)
    @action(detail=True, methods=['PATCH'], permission_classes=[IsOwnerOrReadOnly])
    def confirm_purchase(self, request, pk=None):
        # pk는 URL에서 받아온 값으로 배송 ID입니다.
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
        

    def destroy(self, request, *args, **kwargs):
        # pk는 URL에서 받아온 값으로 배송 ID입니다.
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
    permission_classes = [permissions.IsAuthenticated]  # Add appropriate permissions
