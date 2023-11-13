# models.py
from django.utils import timezone
from django.db import models
from accounts.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from geopy.distance import distance

#게시글
class Delivery(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, verbose_name="글제목")
    created_at = models.DateTimeField(verbose_name="구매 날짜와 시각", auto_now_add=True)
    location = models.CharField(max_length=100, verbose_name="위치")
    price = models.IntegerField(verbose_name="최소주문금액", null=False) 
    link = models.CharField(max_length=100, verbose_name="배달지점링크")
    image = models.ImageField(verbose_name='작성이미지', blank=True, null=True, upload_to='post-image')
    content = models.CharField(max_length=100, verbose_name="내용")
    is_completed = models.BooleanField(default=False) # False: 거래 중 / True: 거래 완료
    is_liked = models.BooleanField(default=False)
    latitude = models.FloatField(max_length=100,null=False)
    longitude = models.FloatField(max_length=100, null=False)

class Grocery(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=100)
    unit = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to="post_img")
    buy_time = models.CharField(max_length=100, null=True)
    recruitment_num = models.IntegerField(null=True)
    post_type = models.BooleanField(default=False) # False: 팔아요 / True: 같이 사요
    is_completed = models.BooleanField(default=False) # False: 거래 중 / True: 거래 완료
    is_liked = models.BooleanField(default=False)
    latitude = models.FloatField(max_length=100,null=False)
    longitude = models.FloatField(max_length=100, null=False)

    def __str__(self):
        return self.title

#최근검색어
class RecentSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    query = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    MAX_RECENT_SEARCHES = 10

    class Meta:
        ordering = ['-created_at']

    @classmethod
    def add_search(cls, user, query):
        if user.is_authenticated and query:
            # 해당 사용자의 검색어 개수 확인
            recent_searches_count = cls.objects.filter(user=user).count()

            # 최대 개수 초과 시 오래된 검색어 삭제 후 추가
            if recent_searches_count >= cls.MAX_RECENT_SEARCHES:
                cls.objects.filter(user=user).earliest('created_at').delete()

            recent_search = cls(user=user, query=query)
            recent_search.save()

#댓글
class DeliveryComment(models.Model):
    post = models.ForeignKey(Delivery, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    content = models.TextField(max_length=100)

    def __str__(self):
        return self.content

class GroceryComment(models.Model):
    post = models.ForeignKey(Grocery, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    content = models.TextField(max_length=100)

    def __str__(self):
        return self.content  

#좋아요
class GroceryLike(models.Model):
    post = models.ForeignKey(Grocery, null=True, on_delete=models.CASCADE, related_name='grocery_like')
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='grocery_like')

    def __str__(self):
        return self.user.name
    
class DeliveryLike(models.Model):
    post = models.ForeignKey(Delivery, null=True, on_delete=models.CASCADE, related_name='delivery_like')
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='delivery_like')

    def __str__(self):
        return self.user.name

#신청  
class DeliveryApplication(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    post = models.ForeignKey(Delivery, null=True, on_delete=models.CASCADE, related_name='delivery_applications')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} applied on {self.post}"

class GroceryApplication(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    post = models.ForeignKey(Grocery, null=True, on_delete=models.CASCADE, related_name='grocery_applications')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} applied on {self.post}"
