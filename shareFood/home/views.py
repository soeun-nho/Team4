from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status,  filters
from rest_framework import viewsets,  permissions
from .models import *
from .serializers import *
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import api_view

from rest_framework.views import APIView

from django.db.models import Q
from math import cos, radians

#권한설정
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

#게시글 CRUD
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
    
    # 검색
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']
    
    #게시글 목록 조회 (검색/상태로 필터링)
    def list(self, request, *args, **kwargs):
        search_query = request.query_params.get('search', None)
        is_completed = request.query_params.get('is_completed', None)
        latitude = request.query_params.get('latitude', None)
        longitude = request.query_params.get('longitude', None)
        radius = request.query_params.get('radius', None)


        # 기본 queryset은 모든 게시글
        queryset = self.queryset.all()

        # 검색한 경우 또는 판매 완료 아닌 글만 필터링
        if search_query is not None:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))
    
        if is_completed is not None:
            queryset = queryset.filter(is_completed=is_completed.lower() == 'true')

        #위치 정보를 이용한 필터링
        if latitude is not None and longitude is not None and radius is not None:
        #  # 일반적인 경우의 위치 필터링
        #     queryset = queryset.filter(
        #         latitude__range=(float(latitude) - float(radius), float(latitude) + float(radius)),
        #         longitude__range=(float(longitude) - float(radius), float(longitude) + float(radius)),
        #     )
        # 일반적인 FloatField를 사용하는 경우
            min_latitude = float(latitude) - (float(radius) / 111.32)  # 1도는 약 111.32km
            max_latitude = float(latitude) + (float(radius) / 111.32)
            min_longitude = float(longitude) - (float(radius) / (111.32 * cos(radians(float(latitude)))))
            max_longitude = float(longitude) + (float(radius) / (111.32 * cos(radians(float(latitude)))))

            queryset = queryset.filter(
                latitude__range=(min_latitude, max_latitude),
                longitude__range=(min_longitude, max_longitude),
            )

        # 검색이 이루어졌을 때 최근 검색어를 저장
        if request.user.is_authenticated and search_query is not None:
            RecentSearchView.add_to_recent_searches(request.user, search_query)

        if not queryset.exists():
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

    #게시글 목록 조회 (검색/상태로 필터링)
    def list(self, request, *args, **kwargs):
        search_query = request.query_params.get('search', None)
        is_completed = request.query_params.get('is_completed', None)
        latitude = request.query_params.get('latitude', None)
        longitude = request.query_params.get('longitude', None)
        radius = request.query_params.get('radius', None)

        
        # 기본 queryset은 모든 게시글
        queryset = self.queryset.all()

        # 검색한 경우 또는 판매 완료 아닌 글만 필터링
        if search_query is not None:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))
    
        if is_completed is not None:
            queryset = queryset.filter(is_completed=is_completed.lower() == 'true')

        #위치 정보를 이용한 필터링
        if latitude is not None and longitude is not None and radius is not None:
        #  # 일반적인 경우의 위치 필터링
        #     queryset = queryset.filter(
        #         latitude__range=(float(latitude) - float(radius), float(latitude) + float(radius)),
        #         longitude__range=(float(longitude) - float(radius), float(longitude) + float(radius)),
        #     )
        # 일반적인 FloatField를 사용하는 경우
            min_latitude = float(latitude) - (float(radius) / 111.32)  # 1도는 약 111.32km
            max_latitude = float(latitude) + (float(radius) / 111.32)
            min_longitude = float(longitude) - (float(radius) / (111.32 * cos(radians(float(latitude)))))
            max_longitude = float(longitude) + (float(radius) / (111.32 * cos(radians(float(latitude)))))

            queryset = queryset.filter(
                latitude__range=(min_latitude, max_latitude),
                longitude__range=(min_longitude, max_longitude),
            )

        # 검색이 이루어졌을 때 최근 검색어를 저장
        if request.user.is_authenticated and search_query is not None:
            RecentSearchView.add_to_recent_searches(request.user, search_query)

        if not queryset.exists():
            return Response({'message': '검색 결과가 없습니다.'}, status=status.HTTP_200_OK)
        
        # 나머지 코드는 그대로 두고 queryset만 변경
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    


#댓글 CR
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

#댓글 UD
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

#게시글 좋아요
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

# #게시글 신청
# class DeliveryApplicationView(APIView):
#     permission_classes = [IsOwnerOrReadOnly]
#     def post(self, request, post_id):
#         post = get_object_or_404(Delivery, pk=post_id)
#         serializer = DeliveryApplicationSerializer(data={'user': request.user.id, 'post': post_id})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class GroceryApplicationView(APIView):
#     permission_classes = [IsOwnerOrReadOnly]
#     def post(self, request, post_id):
#         post = get_object_or_404(Grocery, pk=post_id)
#         serializer = GroceryApplicationSerializer(data={'user': request.user.id, 'post': post_id})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
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

        # GroceryLike 모델에서 user가 현재 사용자인 좋아요 정보 가져오기
        liked_groceries = GroceryLike.objects.filter(user=request.user)
        liked_grocery_ids = liked_groceries.values_list('post_id', flat=True)
        liked_groceries_data = Grocery.objects.filter(id__in=liked_grocery_ids)
        liked_groceries_serializer = GrocerySerializer(liked_groceries_data, many=True)

        # DeliveryLike 모델에서 user가 현재 사용자인 좋아요 정보 가져오기
        liked_deliveries = DeliveryLike.objects.filter(user=request.user)
        liked_delivery_ids = liked_deliveries.values_list('post_id', flat=True)
        liked_deliveries_data = Delivery.objects.filter(id__in=liked_delivery_ids)
        liked_deliveries_serializer = DeliverySerializer(liked_deliveries_data, many=True)

         # 사용자가 신청한 Grocery 게시글 조회
        grocery_applications = GroceryApplication.objects.filter(user=request.user)
        grocery_applications_serializer = GroceryApplicationSerializer(grocery_applications, many=True)

        # 사용자가 신청한 Delivery 게시글 조회
        delivery_applications = DeliveryApplication.objects.filter(user=request.user)
        delivery_applications_serializer = DeliveryApplicationSerializer(delivery_applications, many=True)


        data = {
            'profile': profile_data,
            'grocery_all': grocery_serializer_all.data,
            'grocery_completed': grocery_serializer_completed.data,
            'delivery_all': delivery_serializer_all.data,
            'delivery_completed': delivery_serializer_completed.data,
            'liked_groceries': liked_groceries_serializer.data,
            'liked_deliveries': liked_deliveries_serializer.data,
            'grocery_applications': grocery_applications_serializer.data,
            'delivery_applications': delivery_applications_serializer.data,
        }


        return Response(data, status=status.HTTP_200_OK)

#최근검색어저장
class RecentSearchView(APIView):
    # 최대 저장 검색어 개수
    MAX_RECENT_SEARCHES = 5

    @staticmethod
    def add_to_recent_searches(user, query):
        # 최근 검색어 저장
        RecentSearch.add_search(user, query)
        recent_searches = RecentSearch.objects.filter(user=user).order_by('-created_at')[:RecentSearchView.MAX_RECENT_SEARCHES]
        return [search.query for search in recent_searches]

    @api_view(['GET'])
    def recent_searches_list(request):
        if not request.user.is_authenticated:
            return Response({"message": "로그인을 해주세요."}, status=status.HTTP_401_UNAUTHORIZED)

        search_query = request.query_params.get('search', None)
        recent_searches = RecentSearchView.add_to_recent_searches(request.user, search_query)

        return Response({'recent_searches': recent_searches}, status=status.HTTP_200_OK)
    






#게시글 신청
class DeliveryApplicationView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    
    def post(self, request, post_id):
        post = get_object_or_404(Delivery, pk=post_id)
        serializer = DeliveryApplicationSerializer(data={'post': post_id})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class GroceryApplicationView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    
    def post(self, request, post_id):
        post = get_object_or_404(Grocery, pk=post_id)
        serializer = GroceryApplicationSerializer(data={'post': post_id})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# from django.contrib.gis.geos import Point
# from django.contrib.gis.measure import D
# from .models import Position
# from .serializers import PositionSerializer



# class PositionView(APIView):
#     permission_classes = [IsOwnerOrReadOnly]

#     def get(self, request):
#         user_latitude = float(request.query_params.get('latitude'))
#         user_longitude = float(request.query_params.get('longitude'))

#         user_location = Point(user_longitude, user_latitude, srid=4326)  # SRID는 위경도의 좌표 체계를 의미
        
#         # 반경 내의 위치 가져오기
#         locations_within_radius = Position.objects.filter(geolocation__distance_lte=(user_location, D(km=5)))
#         serializer = PositionSerializer(locations_within_radius, many=True)

#         return Response(serializer.data)


   