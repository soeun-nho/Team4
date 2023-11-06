# Create your views here.
from .models import *
from rest_framework import generics, status
from .serializers import *
from django.shortcuts import redirect,render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

#회원가입 중복확인_최종
class UserRegistration(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#이메일 반환
class FindUserEmailView(APIView):
    def post(self, request, format=None):
        serializer = UserEmailSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            phone = serializer.validated_data['phone']
            
            try:
                user = User.objects.get(name=name, phone=phone)
                return Response({'email': user.email})
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=404)
        else:
            return Response(serializer.errors, status=400)

#비밀번호 반환   
class GetUserPasswordView(APIView):
    def post(self, request, format=None):
        serializer = UserPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            phone = serializer.validated_data['phone']
            name = serializer.validated_data['name']
            
            try:
                user = User.objects.get(email=email, phone=phone, name=name)
                return Response({'password': user.password})
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=404)
        else:
            return Response(serializer.errors, status=400)

# #비밀번호 재설정 이메일 발송
# class SendPasswordResetEmailView(APIView):
#     def post(self, request, format=None):
#         serializer = UserPasswordSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()  # 이 부분에서 비밀번호 재설정 이메일을 보내는 로직이 수행됨
#             return Response({'message': '이메일이 전송되었습니다.'})
#         else:
#             return Response(serializer.errors, status=400)

# #비밀번호 재설정
# class PasswordResetView(APIView):
#     def post(self, request, token):
#         try:
#             user = User.objects.get(auth_token=token)
#         except User.DoesNotExist:
#             return Response({"error": "유효하지 않은 토큰입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
#         new_password = request.data.get('new_password')
#         if new_password:
#             user.password = make_password(new_password)
#             user.save()
#             return Response({"message": "비밀번호가 재설정되었습니다."}, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "새 비밀번호를 제공해주세요."}, status=status.HTTP_400_BAD_REQUEST)

#회원정보 확인
class UserExistence(APIView):
      def post(self, request, format=None):
        serializer = UserExistenceSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            # 유효성 검사를 통과한 경우
            return Response({'message': '사용자 정보가 일치합니다.'})
        else:
            # 유효성 검사를 통과하지 못한 경우
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 비밀번호 수정
class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(login_required)
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            new_password = serializer.validated_data['new_password']

            user.set_password(new_password)
            user.save()
            return Response({"message": "비밀번호가 업데이트되었습니다."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    