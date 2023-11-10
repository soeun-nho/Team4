from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status,  filters
from rest_framework import viewsets,  permissions
from .models import *
from .serializers import *
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


from rest_framework.views import APIView

from django.db.models import Q


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
    
        # 로그인하지 않은 사용자에게 GET 요청을 허용합니다.
        if request.method == 'GET' and not request.user.is_authenticated:
            return True
        return obj.user == request.user

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

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied('로그인이 필요합니다.')
        serializer.save(user=self.request.user)

    
    #상태변경
    @action(detail=True, methods=['PATCH'], permission_classes=[IsOwnerOrReadOnly])
    def confirm_purchase(self, request, pk=None):
        try:
            delivery = self.get_object()
        except Delivery.DoesNotExist:
            return Response({'error': '게시글을 찾을 수 없음.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user == delivery.user:
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

        if request.user == delivery.user:
            delivery.delete()
            return Response({'message': '삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
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


#### Grocery 기능 ####

class GroceryViewSet(viewsets.ModelViewSet):
    queryset = Grocery.objects.all().order_by('-id') # 최근글이 앞으로 오도록 정렬(default)
    serializer_class = GrocerySerializer
    permission_classes = [IsOwnerOrReadOnly]

    #def perform_create(self, serializer):
        #serializer.save(user = self.request.user)

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied('로그인이 필요합니다.')
        serializer.save(user=self.request.user)

    #상태변경
    @action(detail=True, methods=['PATCH'], permission_classes=[IsOwnerOrReadOnly])
    def confirm_purchase(self, request, pk=None):
        try:
            grocery = self.get_object()
        except Grocery.DoesNotExist:
            return Response({'error': '게시글을 찾을 수 없음.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user == grocery.user:
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

        if request.user == grocery.user:
            grocery.delete()
            return Response({'message': '삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': '권한이 없습니다.(작성자가 아님)'}, status=status.HTTP_403_FORBIDDEN)
        

    # 검색 기능 
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    #게시글 목록 조회(검색어필터링가능)
    def list(self, request, *args, **kwargs):
        search_query = request.query_params.get('search', None)

        if search_query is not None:
            queryset = self.queryset.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))
        else:
            queryset = self.queryset  # 검색어가 없으면 모든 결과를 반환

        if not queryset.exists():
            return Response({'message': '검색 결과가 없습니다.'}, status=status.HTTP_200_OK)
        
        # 나머지 코드는 그대로 두고 queryset만 변경
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


## grocery 댓글 기능 ##

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


class GroceryCommentDetailView(APIView):
    permission_classes = [IsCommentAuthorOrReadOnly]
    
    def patch(self, request, post_id, comment_id):
        comment = get_object_or_404(GroceryComment, pk=comment_id)
        
        # 댓글 작성자만 수정할 수 있도록 검사
        if comment.user == request.user:
            serializer = GroceryCommentSerializer(comment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(user=request.user, post_id=post_id)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': '댓글 작성자만 수정할 수 있습니다.'}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, post_id, comment_id):
        comment = get_object_or_404(GroceryComment, pk=comment_id)

        # 댓글 작성자만 삭제할 수 있도록 검사
        if comment.user == request.user:
            comment.delete()
            return Response({'message': '삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': '댓글 작성자만 삭제할 수 있습니다.'}, status=status.HTTP_403_FORBIDDEN)





#### Delivery 댓글 기능  ####

class DeliveryCommentView(APIView):   # 댓글 리스트
    permission_classes = [IsCommentAuthorOrReadOnly]

    def get(self, request, post_id):
        comment = DeliveryComment.objects.filter(post=post_id)
        serializer = DeliveryCommentSerializer(comment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, post_id):
        serializer = DeliveryCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post_id=post_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


class DeliveryCommentDetailView(APIView):
    permission_classes = [IsCommentAuthorOrReadOnly]
    
    def patch(self, request, post_id, comment_id):
        comment = get_object_or_404(DeliveryComment, pk=comment_id)
        
        # 댓글 작성자만 수정할 수 있도록 검사
        if comment.user == request.user:
            serializer = DeliveryCommentSerializer(comment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(user=request.user, post_id=post_id)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': '댓글 작성자만 수정할 수 있습니다.'}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, post_id, comment_id):
        comment = get_object_or_404(DeliveryComment, pk=comment_id)

        # 댓글 작성자만 삭제할 수 있도록 검사
        if comment.user == request.user:
            comment.delete()
            return Response({'message': '삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': '댓글 작성자만 삭제할 수 있습니다.'}, status=status.HTTP_403_FORBIDDEN)


### Grocery 좋아요 기능 ###

# class GroceryLikeView(APIView):
#     permission_classes = [IsOwnerOrReadOnly]

#     def post(self, request, post_id):
#         post = get_object_or_404(Grocery, pk=post_id)
#         serializer = GroceryLikeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user, post=post)
#             post.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

class GroceryLikeView(APIView):   # 게시글 좋아요
    permission_classes = [IsOwnerOrReadOnly]
    
    def post(self, request, post_id):
        post = get_object_or_404(Grocery, pk=post_id)
        serializer = GroceryLikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            post.is_liked = False if post.is_liked else True
            post.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)



### Delivery 좋아요 기능 ###

class DeliveryLikeView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def post(self, request, post_id):
        post = get_object_or_404(Delivery, pk=post_id)
        serializer = DeliveryLikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            post.is_liked = False if post.is_liked else True
            post.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
        


# 마이페이지
class UserProfileView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"message": "로그인을 해주세요."}, status=status.HTTP_401_UNAUTHORIZED)

        user = request.user

        profile_data = {
            'id' : user.id,
            'name' : user.name,
            'email': user.email,
            'phone': user.phone,
        }

         # Grocery 모델에서 모든 데이터 가져오기
        grocery_all = Grocery.objects.filter(user=request.user)
        grocery_serializer_all = GrocerySerializer(grocery_all, many=True)

        # Delivery 모델에서 모든 데이터 가져오기
        delivery_all = Delivery.objects.filter(user=request.user)
        delivery_serializer_all = DeliverySerializer(delivery_all, many=True)

        # Grocery 모델에서 is_completed=True인 데이터만 필터링
        grocery_completed = grocery_all.filter(is_completed=True)
        grocery_serializer_completed = GrocerySerializer(grocery_completed, many=True)

        # Delivery 모델에서 is_completed=True인 데이터만 필터링
        delivery_completed = delivery_all.filter(is_completed=True)
        delivery_serializer_completed = DeliverySerializer(delivery_completed, many=True)

        data = {
            'profile': profile_data,
            'grocery_all': grocery_serializer_all.data,
            'grocery_completed': grocery_serializer_completed.data,
            'delivery_all': delivery_serializer_all.data,
            'delivery_completed': delivery_serializer_completed.data,
        }


        return Response(data, status=status.HTTP_200_OK)
