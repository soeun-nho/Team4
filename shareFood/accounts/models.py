from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, name, phone, email, password=None, register=False):
        if not name:
            raise ValueError('must have user name')
        if not phone:
            raise ValueError('must have user phone')
        if not email:
            raise ValueError('must have user name')
        # try:
        #     validate_email(email)  # Validate email format
        # except ValidationError:
        #     raise ValueError('invalid email format')
        
        user = self.model(
            name = name,
            phone = phone,
            email = email,
            register = register,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, name, phone, email, password=None):
        user = self.create_user(
            name = name,
            phone = phone,
            email = email,
        )
        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    name = models.CharField(default='', max_length=100, null=False, blank=False)
    phone = models.CharField(default='', max_length=100, null=False, blank=False, unique=True)
    email = models.CharField(default='', max_length=100, null=False, blank=False, unique=True)
    register = models.BooleanField(verbose_name="간편 결제 등록 여부", default=False)
    #password_check = models.CharField(default='', max_length=100, null=False, blank=False)
    # User 모델의 필수 field
    is_active = models.BooleanField(default=True)   
    is_admin = models.BooleanField(default=False)
    # 헬퍼 클래스 사용
    objects = UserManager()
    # 사용자의 username field는 email로 설정
    USERNAME_FIELD = 'email'
    # 필수로 작성해야하는 field
    REQUIRED_FIELDS = ['phone', 'name']

    #객체 문자열로 표현
    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    #사용자가 스태프인지 확인_ is_admin이 True면 is_staff도 True
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
