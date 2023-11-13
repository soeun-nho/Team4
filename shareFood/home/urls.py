from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

app_name = 'home'


router = DefaultRouter()
router.register(r'groceries', GroceryViewSet)
router.register(r'deliveries', DeliveryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    #최근검색어
    path('api/recent-searches/', RecentSearchView.recent_searches_list, name='recent-searches-list'), 
    #댓글 C,R
    path('deliveries/<int:post_id>/comments/', DeliveryCommentView.as_view(), name='delivery-comments-list'),
    path('groceries/<int:post_id>/comments/', GroceryCommentView.as_view(), name='grocery-comments-list'),
    #댓글 U,D
    path('deliveries/<int:post_id>/comments/<int:comment_id>/', DeliveryCommentDetailView.as_view(), name='delivery-comments-create'),
    path('groceries/<int:post_id>/comments/<int:comment_id>/', GroceryCommentDetailView.as_view(), name='delivery-comments-create'),
    # 좋아요
    path('groceries/<int:post_id>/like/', GroceryLikeView.as_view()),
    path('deliveries/<int:post_id>/like/', DeliveryLikeView.as_view()),
    #신청
    path('apply/delivery/<int:post_id>/', DeliveryApplicationView.as_view(), name='delivery-application'),
    path('apply/grocery/<int:post_id>/', GroceryApplicationView.as_view(), name='grocery-application'),
    #마이페이지
    path('mypage/', UserProfileView.as_view(), name='mypage'),
]