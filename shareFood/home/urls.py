from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeliveryViewSet

router = DefaultRouter()
# router.register(r'groceries', GroceryViewSet)
router.register(r'deliveries', DeliveryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('deliveries/<int:delivery_id>/', DeliveryViewSet.as_view({'get': 'retrieve'}), name='delivery-detail'),

]