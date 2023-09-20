from django.urls import path

from apps.post.pages.posts.views import (
    CreatePost,
    like_post,
    download_replies,
    create_reply,
    DownloadPosts,
    PostListView,
    FilterPosts,
    SearchPosts,
)

app_name = 'post'

urlpatterns = [
    path('posts/', PostListView.as_view(), name='list'),
    path('posts/like_post/', like_post, name='like_post'),
    path('posts/create_reply/', create_reply, name='create_reply'),
    path('posts/download_replies/', download_replies,
         name='download_replies'),
    path('posts/download/', DownloadPosts.as_view(), name='download_posts'),
    path('posts/create/', CreatePost.as_view(), name='create'),
    path('posts/search/', SearchPosts.as_view(), name='search_posts'),
    path('posts/filter/', FilterPosts.as_view(), name='filter_posts'),
]
