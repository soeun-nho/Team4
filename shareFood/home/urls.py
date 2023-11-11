from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

app_name = 'home'


router = DefaultRouter()
router.register(r'groceries', GroceryViewSet)
router.register(r'deliveries', DeliveryViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # 배달 댓글 조회, 생성
    path('deliveries/<int:post_id>/comments/', DeliveryCommentView.as_view(), name='delivery-comments-list'),
    # 배달 댓글 삭제, 수정
    path('deliveries/<int:post_id>/comments/<int:comment_id>/', DeliveryCommentDetailView.as_view(), name='delivery-comments-create'),

    # 식료품 댓글 조회, 생성
    path('groceries/<int:post_id>/comments/', GroceryCommentView.as_view(), name='grocery-comments-list'),
    # 식료품 댓글 삭제, 수정
    path('groceries/<int:post_id>/comments/<int:comment_id>/', GroceryCommentDetailView.as_view(), name='delivery-comments-create'),
    path('groceries/<int:post_id>/location/', GroceryNearInfoView.as_view()),
    path('deliveries/<int:post_id>/location/', DeliveryNearInfoView.as_view()),


    # 식료품 좋아요 기능
    path('groceries/<int:post_id>/like/', GroceryLikeView.as_view()),

    # 배달 좋아요 기능
    path('deliveries/<int:post_id>/like/', DeliveryLikeView.as_view()),

    #사용자 신청
    path('apply/delivery/<int:post_id>/', DeliveryApplicationView.as_view(), name='delivery-application'),
    path('apply/grocery/<int:post_id>/', GroceryApplicationView.as_view(), name='grocery-application'),

    #마이페이지 _ 내게시글
    path('mypage/', UserProfileView.as_view(), name='mypage'),
    
    #최근검색어
    path('api/recent-searches/', RecentSearchView.recent_searches_list, name='recent-searches-list'),
]