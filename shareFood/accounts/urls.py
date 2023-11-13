from django.urls import path, include
from . import views
from rest_framework import urls
# from dj_rest_auth.views import LoginView

urlpatterns =[
    path('signup/', views.UserRegistration.as_view()),
    #path('customlogin/', views.CustomLoginView.as_view(), name='custom-login'), 커스텀로그인(시도중)
    path('', include('dj_rest_auth.urls')),
]