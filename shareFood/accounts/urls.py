from django.urls import path, include
from . import views
from rest_framework import urls

urlpatterns =[
    path('signup/', views.UserRegistration.as_view()),
    path('', include('dj_rest_auth.urls')),
    # path('api/forgot-email/', views.FindUserEmailView.as_view(), name='find-user-email'),
    # path('api/forgot-password/', views.GetUserPasswordView.as_view(), name='get-user-password'),
    # path('api/user-info/', views.UserExistence.as_view(), name='check-user-existence'),
    # path('api/change-password/', views.ChangePassword.as_view(), name='change-password'),
]