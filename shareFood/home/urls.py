from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

app_name = 'home'


router = DefaultRouter()
router.register(r'groceries', GroceryViewSet)
router.register(r'deliveries', DeliveryViewSet)


urlpatterns = [
    path('', include(router.urls)),
     # 배달 게시물에 대한 댓글 목록 조회
    path('deliveries/<int:id>/comments/', DeliveryCommentViewSet.as_view({'get': 'list'}), name='delivery-comments-list'),
    # 배달 게시물에 댓글 생성
    path('deliveries/<int:id>/comments/', DeliveryCommentViewSet.as_view({'post': 'create'}), name='delivery-comments-create'),

    # 식료품 댓글 조회, 생성
    path('groceries/<int:post_id>/comments/', GroceryCommentView.as_view(), name='grocery-comments-list'),
    # 식료품 댓글 삭제, 수정
    path('groceries/<int:post_id>/comments/<int:comment_id>/', GroceryCommentDetailView.as_view(), name='delivery-comments-create'),
]