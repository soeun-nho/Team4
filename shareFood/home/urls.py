from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

app_name = 'home'

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'groceries', GroceryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('comments/', include(router.urls)),
]