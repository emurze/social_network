from django.urls import path

from apps.post.pages.posts.views import (
    CreatePost,
    like_post,
    download_replies,
    CreteReply,
    download_posts,
    ResetPosts,
    PostListView,
    FilterPosts,
    SearchPosts,
)

app_name = 'post'

urlpatterns = [
    path('posts/', PostListView.as_view(), name='list'),
    path('posts/like/', like_post, name='like_post'),
    path('posts/create/', CreatePost.as_view(), name='create'),
    path('posts/search/', SearchPosts.as_view(), name='search_posts'),
    path('posts/filter/', FilterPosts.as_view(), name='filter_posts'),
    path('posts/download/', download_posts, name='download_posts'),
    path('posts/reset/', ResetPosts.as_view(), name='reset_posts'),
    path('posts/create_reply/', CreteReply.as_view(), name='create_reply'),
    path('posts/download_replies/', download_replies, name='download_replies'),
]
