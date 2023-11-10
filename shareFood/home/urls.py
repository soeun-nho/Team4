from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

app_name = 'home'


router = DefaultRouter()
router.register(r'groceries', GroceryViewSet)
router.register(r'deliveries', DeliveryViewSet)
# router.register(r'my-posts', MyPostsViewSet, basename='my-posts')

urlpatterns = [
    path('', include(router.urls)),

    # 배달 댓글 조회, 생성
    path('deliveries/<int:post_id>/comments/', DeliveryCommentView.as_view, name='delivery-comments-list'),
    # 배달 댓글 삭제, 수정
    path('deliveries/<int:post_id>/comments/', DeliveryCommentDetailView.as_view, name='delivery-comments-create'),

    # 식료품 댓글 조회, 생성
    path('groceries/<int:post_id>/comments/', GroceryCommentView.as_view(), name='grocery-comments-list'),
    # 식료품 댓글 삭제, 수정
    path('groceries/<int:post_id>/comments/<int:comment_id>/', GroceryCommentDetailView.as_view(), name='delivery-comments-create'),

    # path('deliveries/recentsearch/', DeliveryViewSet.as_view({'get': 'recent_searches_list'}), name='recent_search_list'),
    
    # 식료품 좋아요 기능
    path('groceries/<int:post_id>/like/', GroceryLikeView.as_view()),

    # 배달 좋아요 기능
    path('deliveries/<int:post_id>/like/', DeliveryLikeView.as_view()),
    
 

]