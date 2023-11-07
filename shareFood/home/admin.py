from django.contrib import admin

# Register your models here.
from .models import Grocery, GroceryComment, Delivery

admin.site.register(Grocery)
admin.site.register(GroceryComment)
admin.site.register(Delivery)