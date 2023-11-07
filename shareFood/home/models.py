from django.db import models
from accounts.models import User

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


class GroceryComment(models.Model):
    post = models.ForeignKey(Grocery, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    content = models.TextField(max_length=100)

    def __str__(self):
        return self.content
    

class Delivery(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, verbose_name="글제목")
    created_at = models.DateTimeField(verbose_name="구매 날짜와 시각", auto_now_add=True)
    location = models.CharField(max_length=100, verbose_name="위치")
    minimumPrice = models.IntegerField(verbose_name="최소주문금액", default=0)
    link = models.CharField(max_length=100, verbose_name="배달지점링크")
    image = models.ImageField(verbose_name='작성이미지', blank=True, null=True, upload_to='post-image')
    content = models.CharField(max_length=100, verbose_name="내용")
