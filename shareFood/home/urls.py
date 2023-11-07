from django.urls import path
from .views import *

app_name = 'home'

urlpatterns = [
    path('', GroceryView.as_view()),
    path('<int:post_id>/', GroceryDetailView.as_view()),
    path('<int:post_id>/comment/', GroceryCommentView.as_view()),
    path('<int:post_id>/comment/<int:comment_id>/', GroceryCommentDetailView.as_view()),
]