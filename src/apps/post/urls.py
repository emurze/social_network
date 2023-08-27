from django.urls import path

from apps.post.features.detail.views import PostDetailView
from apps.post.features.list.views import PostListView

app_name = 'post'

urlpatterns = [
    path('posts/', PostListView.as_view(), name='list'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='detail'),
]
