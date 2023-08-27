from django.views.generic import DetailView

from apps.post.models import Post


class PostDetailView(DetailView):
    template_name = 'post/detail.html'
    context_object_name = 'post'
    model = Post
