from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model #커스텀사용자
user = get_user_model()

admin.site.register(user) 