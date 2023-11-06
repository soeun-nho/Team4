from django.db import models

# Create your models here.
# class Delivery(models.Model):
#     customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     title = models.CharField(verbose_name="글제목")
#     created_at = models.DateTimeField(verbose_name="구매 날짜와 시각", auto_now_add=True)
#     location = models.CharField(verbose_name="위치")
#     minimumPrice = models.IntegerField(verbose_name="최소주문금액", default=0)
#     link=models.CharField(verbose_name="배달지점링크")
#     image = models.ImageField(verbose_name='작성이미지', blank=True, null=True, upload_to='post-image')
#     content = models.CharField(verbose_name="내용")