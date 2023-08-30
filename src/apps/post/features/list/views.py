from django.db.models import QuerySet
from django.views.generic import ListView

from apps.post.models import Post


class PostListView(ListView):
    template_name = 'post/posts/posts.html'
    context_object_name = 'posts'

    def get_queryset(self) -> QuerySet[Post]:
        return Post.objects.all()[:4]

