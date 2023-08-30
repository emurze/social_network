import enum
import logging

from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet, Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from apps.post.models import Post

lg = logging.getLogger(__name__)


class LikeAction(enum.StrEnum):
    LIKE = 'like'
    UNLIKE = 'unlike'


class LikeActionListMixin:
    def get_context_data(self, *args, **kwargs):
        posts = self.object_list
        my_user = self.request.user

        for post in posts:
            if post.liked_users.contains(my_user):
                post.action = LikeAction.UNLIKE
            else:
                post.action = LikeAction.LIKE

        return super().get_context_data(*args, **kwargs)


def like_list(request: WSGIRequest) -> JsonResponse:
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    my_user = request.user

    action = request.POST.get('action')
    match action:
        case LikeAction.LIKE:
            post.liked_users.add(my_user)
            action = LikeAction.UNLIKE

        case LikeAction.UNLIKE:
            post.liked_users.remove(my_user)
            action = LikeAction.LIKE

    return JsonResponse({'action': action})


class PostListView(LikeActionListMixin, ListView):
    template_name = 'post/posts/posts.html'
    context_object_name = 'posts'

    def get_queryset(self) -> QuerySet[Post]:
        return (Post.objects
                .annotate(likes_count=Count('liked_users'))
                .order_by('-created')[:4])

