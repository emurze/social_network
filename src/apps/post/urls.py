from django.urls import path

from apps.post.features.list.views import PostListView, like_list

app_name = 'post'

urlpatterns = [
    path('posts/', PostListView.as_view(), name='users'),
    path('posts/like_list/', like_list, name='like_list'),
]
