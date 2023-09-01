import enum
import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import DetailView

from apps.account.mixins import ProfileSelectedMixin
from apps.account.services.follow.dispatcher import dispatch_follow_action
from apps.account.services.follow.mixins import FollowActionDetailMixin
from apps.post.features.list.forms import ReplyForm

User = get_user_model()
lg = logging.getLogger(__name__)


class AddRepliesWithoutFirstMixin:
    def get_context_data(self, *args, **kwargs):
        user = self.object
        posts = kwargs.get('user_posts', user.posts.all())

        posts = posts.annotate(
            likes_count=Count('liked_users', distinct=True),
            reply_count=Count('replies', distinct=True),
        )

        for post in posts:
            replies = post.replies.all()

            post.replies_first = replies.first()
            post.replies_without_first = replies[1:]

        kwargs['user_posts'] = posts
        return super().get_context_data(*args, **kwargs)


class LikeAction(enum.StrEnum):
    LIKE = 'like'
    UNLIKE = 'unlike'


class LikeActionAccountDetailMixin:
    def get_context_data(self, *args, **kwargs):
        user = self.object
        posts = kwargs.get('user_posts', user.posts.all())
        my_user = self.request.user

        for post in posts:
            if post.liked_users.contains(my_user):
                post.action = LikeAction.UNLIKE
            else:
                post.action = LikeAction.LIKE

        kwargs['user_posts'] = posts
        return super().get_context_data(*args, **kwargs)


@login_required
@require_POST
def follow_detail(request: WSGIRequest, username: str) -> JsonResponse:
    action = dispatch_follow_action(
        action=request.POST.get('action'),
        my_user=request.user,
        other_user=get_object_or_404(User, username=username)
    )
    return JsonResponse({'action': action})


class AccountDetailView(
    LoginRequiredMixin,
    ProfileSelectedMixin,
    FollowActionDetailMixin,
    AddRepliesWithoutFirstMixin,
    LikeActionAccountDetailMixin,
    DetailView
):
    model = User
    template_name = 'account/profile/profile.html'
    context_object_name = 'user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    extra_context = {'reply_form': ReplyForm()}
