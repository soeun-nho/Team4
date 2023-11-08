from django.shortcuts import render, get_object_or_404
from .models import GroceryComment, Grocery, Delivery
from rest_framework import status
from rest_framework.response import Response
from .serializers import GrocerySerializer, GroceryCommentSerializer

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import viewsets, permissions


# 글의 작성자만 수정 권한
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 읽기 권한 요청이 들어오면 인증여부 상관없이 허용 (GET)
        if request.method in permissions.SAFE_METHODS:
            return True

        # 요청자(request.user)가 객체의 user와 동일한지 확인 (PUT, DELETE)
        return obj.user == request.user


# ModelViewSet: 필터, 검색, 정렬 용이
class GroceryViewSet(viewsets.ModelViewSet):
    queryset = Grocery.objects.all().order_by('-id') # 최근글이 앞으로 오도록 정렬(default)
    serializer_class = GrocerySerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


    # 거래 확정
    @action(detail=True, methods=['PATCH'], permission_classes=[permissions.IsAuthenticated])
    def confirm_purchase(self, request, pk=None):
        grocery = self.get_object()

        if request.user == grocery.customer:
            grocery.is_completed = True
            grocery.save()
            return Response({'status': '거래가 확정되었습니다.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
    
