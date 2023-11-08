from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

app_name = 'home'


router = DefaultRouter()
router.register(r'groceries', GroceryViewSet)
router.register(r'deliveries', DeliveryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('comments/', include(router.urls)),
]