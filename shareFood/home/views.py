from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

# Create your views here.
from rest_framework import viewsets,  permissions
from .models import Delivery
from .serializers import DeliverySerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    글의 작성자만 수정 권한을 가짐.
    """

    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모두에게 허용.
        if request.method in permissions.SAFE_METHODS:
            return True

        # 쓰기 권한은 글의 작성자에게만 허용.
        return obj.customer == request.user
    
class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    # permission_classes = [permissions.IsAuthenticated]  # 인증된 사용자만 허용
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # 게시글 작성 시, 현재 사용자를 게시글의 customer 필드에 할당
        serializer.save(customer=self.request.user)

    @action(detail=True, methods=['PATCH'], permission_classes=[permissions.IsAuthenticated])
    def confirm_purchase(self, request, pk=None):
        delivery = self.get_object()

        # 요청을 보낸 사용자가 글의 작성자인지 확인
        if request.user == delivery.customer:
            delivery.is_completed = True  # 구매 확정을 True로 설정
            delivery.save()
            return Response({'status': '구매가 확정되었습니다.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)