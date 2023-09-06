import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import DetailView

from apps.account.features.detail.mixins import AddUserPosts, \
    LikeActionAccountDetailMixin
from apps.account.mixins import ProfileSelectedMixin
from apps.account.services.follow.dispatcher import dispatch_follow_action
from apps.account.services.follow.mixins import FollowActionDetailMixin
from apps.post.features.list.mixins import AddReplyFormMixin, AddPostForm

User = get_user_model()
lg = logging.getLogger(__name__)


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
    AddUserPosts,
    AddPostForm,
    AddReplyFormMixin,
    LikeActionAccountDetailMixin,
    DetailView
):
    model = User
    template_name = 'account/profile/profile.html'
    context_object_name = 'user'
    slug_field = 'username'
    slug_url_kwarg = 'username'


@login_required
@require_GET
def follow_pagination(request: WSGIRequest) -> HttpResponse:
    lg.debug(request.GET)

    if ():
        return HttpResponse('')
    return render(request, '')
