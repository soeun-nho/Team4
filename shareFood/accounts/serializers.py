from .models import User
from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
#회원가입 중복 확인
class UserSerializer(serializers.ModelSerializer):
    password_check = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'name', 'password_check', 'password', 'phone')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['password_check']:
            raise serializers.ValidationError("비밀번호와 비밀번호 확인이 일치하지 않습니다.")
        try:
            validate_email(data['email'])  # Validate email format
        except ValidationError:
            raise serializers.ValidationError("invalid email format")
        return data

    def create(self, validated_data):
        validated_data.pop('password_check') #유효성 검사 후 삭제
        user = User.objects.create_user(**validated_data)
        return user