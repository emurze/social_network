from django.urls import path

from apps.post.features.list.views import PostListView, like_list, reply_list

app_name = 'post'

urlpatterns = [
    path('posts/', PostListView.as_view(), name='users'),
    path('posts/like_list/', like_list, name='like_list'),
    path('posts/reply/', reply_list, name='reply_list'),
]
