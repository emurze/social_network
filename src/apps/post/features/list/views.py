import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from rest_framework.generics import get_object_or_404

from apps.post.features.list.forms import ReplyForm
from apps.post.models import Post, Reply
from apps.post.services.like.dispatcher import dispatch_like_action
from apps.post.services.like.mixins import LikeActionListMixin

lg = logging.getLogger(__name__)


class PostListView(LoginRequiredMixin, LikeActionListMixin, ListView):
    template_name = 'post/posts/posts.html'
    context_object_name = 'posts'
    extra_context = {'reply_form': ReplyForm()}

    def get_queryset(self) -> QuerySet[Post]:
        return (Post.objects
                .annotate(likes_count=Count('liked_users'))
                .order_by('-created')[:4])

    def get_context_data(self, *args, **kwargs):
        posts = self.object_list

        for post in posts:
            post.replies_without_first = post.replies.all()[1:]

        return super().get_context_data(*args, **kwargs)


def like_list(request: WSGIRequest) -> JsonResponse:
    post_id = request.POST.get('post_id')

    action = dispatch_like_action(
        action=request.POST.get('action'),
        post=get_object_or_404(Post, id=post_id),
        my_user=request.user,
    )

    return JsonResponse({'action': action})


@require_POST
def reply_list(request: WSGIRequest) -> JsonResponse:
    if (form := ReplyForm(request.POST)).is_valid():
        cd = form.cleaned_data
        post_id = request.POST.get('post_id')

        Reply.objects.create(
            content=cd['content'],
            post=get_object_or_404(Post, id=post_id),
            user=request.user,
            parent=cd['parent'],
        )
    else:
        lg.warning(f'Reply errors {form.errors}')

    return JsonResponse({})
