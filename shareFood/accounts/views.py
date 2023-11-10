# Create your views here.
from .models import *
from rest_framework import generics, status
from .serializers import *
from django.shortcuts import redirect,render
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
#from dj_rest_auth.views import LoginView #dj_rest_auth
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from home.models import Grocery, Delivery
from home.serializers import GrocerySerializer, DeliverySerializer

#회원가입
class UserRegistration(APIView):
    permission_classes = [AllowAny] #이 부분 추가
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
