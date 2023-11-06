from django.contrib import admin
#admin site에 커스텀 사용자 등록
from django.contrib.auth import get_user_model #함수 이용해서 가져옴
user = get_user_model()
admin.site.register(user) #관리자사이트에 등록