from django.urls import path

from apps.post.pages.posts.views import (
    create_post,
    like_post,
    download_replies,
    create_reply,
    download_posts,
    PostListView,
    search_posts, filter_posts,
)

app_name = 'post'

urlpatterns = [
    path('posts/', PostListView.as_view(), name='list'),
    path('posts/like_post/', like_post, name='like_post'),
    path('posts/create_reply/', create_reply, name='create_reply'),
    path('posts/download_replies/', download_replies,
         name='download_replies'),
    path('posts/download_posts/', download_posts, name='download_posts'),
    path('posts/create/', create_post, name='create'),
    path('posts/search_posts/', search_posts, name='search_posts'),
    path('posts/filter_posts/', filter_posts, name='filter_posts'),
]
