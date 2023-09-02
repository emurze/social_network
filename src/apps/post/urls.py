from django.urls import path

from apps.post.features.list.views import (
    execute_like_action,
    download_replies_by_slice,
    create_reply, download_posts, PostListView,
)

app_name = 'post'

urlpatterns = [
    path('posts/', PostListView.as_view(), name='list'),
    path('posts/execute_like_action/', execute_like_action,
         name='execute_like_action'),
    path('posts/create_reply/', create_reply, name='create_reply'),
    path('posts/download_replies_by_slice/', download_replies_by_slice,
         name='download_replies_by_slice'),
    path('posts/download_posts/', download_posts, name='download_posts')
]
