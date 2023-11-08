from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status,  filters
from rest_framework import viewsets,  permissions
from .models import *
from .serializers import *
from rest_framework import permissions
from django.db.models import Q

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # return obj.writer == request.user
        # 로그인하지 않은 사용자에게 GET 요청을 허용합니다.
        if request.method == 'GET' and not request.user.is_authenticated:
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
    
    # 검색 기능 
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']
    
    # # 최근 검색어 저장
    # def add_to_recent_searches(self, user, query):
    #     RecentSearch.add_search(user, query)
    #     recent_searches = RecentSearch.objects.filter(user=user).order_by('-created_at')[:RecentSearch.MAX_RECENT_SEARCHES]
    #     self.recent_searches = [search.query for search in recent_searches]

    # # 최근 검색어 반환
    # @action(detail=False, methods=['get'])
    # def recent_searches_list(self, request):
    #     if not request.user.is_authenticated :
    #         return Response({"message" : "로그인을 해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        
    #     self.add_to_recent_searches(request.user, None)
    #     recent_searches = RecentSearch.objects.filter(user=request.user).order_by('-created_at')[:RecentSearch.MAX_RECENT_SEARCHES]
    #     searches = [search.query for search in recent_searches]
    #     return Response(searches, status=status.HTTP_200_OK)

    #게시글 목록 조회(검색어필터링가능)
    def list(self, request, *args, **kwargs):
        search_query = request.query_params.get('search', None)

        if search_query:
            queryset = self.queryset.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))
        else:
            queryset = self.queryset  # 검색어가 없으면 모든 결과를 반환

        if not queryset:
            return Response({'message': '검색 결과가 없습니다.'}, status=status.HTTP_200_OK)
        
        # 나머지 코드는 그대로 두고 queryset만 변경
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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
        except Delivery.DoesNotExist:
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
        except Delivery.DoesNotExist:
            return Response({'error': '게시글을 찾을 수 없음.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user == grocery.writer:
            grocery.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': '권한이 없습니다.(작성자가 아님)'}, status=status.HTTP_403_FORBIDDEN)
        

