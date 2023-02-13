from django.urls import path
from .views import *

app_name = "blog"

urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('add-new-post/', AddPostView.as_view(), name="add_post"),
    path('post/<int:pk>/<str:ref>/', Detail.as_view(), name="post"),
    path('post/edit/<int:pk>/', edit_post, name="edit_post"),
    path('post/delete/<int:pk>/', delete, name="delete_post"),
    path('post/like/', likepost, name="like"),
    path('post/quote/<int:pk>/', Quote_Post, name="quote_post"),
    path('post/retweet/<int:pk>', Retweet, name="retweet_post"),
]