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
    is_liked = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class GroceryComment(models.Model):
    post = models.ForeignKey(Grocery, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    content = models.TextField(max_length=100)

    def __str__(self):
        return self.content
    

class Delivery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, verbose_name="글제목")
    created_at = models.DateTimeField(verbose_name="구매 날짜와 시각", auto_now_add=True)
    location = models.CharField(max_length=100, verbose_name="위치")
    minimumPrice = models.IntegerField(verbose_name="최소주문금액", null=False) 
    link = models.CharField(max_length=100, verbose_name="배달지점링크")
    image = models.ImageField(verbose_name='작성이미지', blank=True, null=True, upload_to='post-image')
    content = models.CharField(max_length=100, verbose_name="내용")
    is_completed = models.BooleanField(default=False) # False: 거래 중 / True: 거래 완료
    is_liked = models.BooleanField(default=False)


class DeliveryComment(models.Model):
    post = models.ForeignKey(Delivery, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    content = models.TextField(max_length=100)

    def __str__(self):
        return self.content
    

class RecentSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # 사용자와 연결
    query = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    MAX_RECENT_SEARCHES = 10 # 각 사용자별로 최대 유지할 검색어 개수

    class Meta:
        ordering = ['-created_at']

    @classmethod
    def add_search(cls, user, query):  # 사용자 정보를 추가로 받도록 수정
        if query:
            # 해당 사용자의 검색어 개수 확인
            recent_searches_count = cls.objects.filter(user=user).count()

            # 최대 개수 초과 시 오래된 검색어 삭제 후 추가
            if recent_searches_count >= cls.MAX_RECENT_SEARCHES:
                cls.objects.filter(customer=user).earliest('created_at').delete()

            recent_search = cls(user=user, query=query)
            recent_search.save()

#### grocery 좋아요 기능 ####

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