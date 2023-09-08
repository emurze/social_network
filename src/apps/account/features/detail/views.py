import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import DetailView

from apps.account.features.detail.mixins import AddUserPosts, \
    LikeActionAccountDetailMixin, AddFollowingUsersMixin
from apps.account.features.detail.services.get_followings_paginator import \
    get_followings_paginator
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
    AddFollowingUsersMixin,
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
def follow_pagination(request: WSGIRequest, user_id: int) -> HttpResponse:
    user = get_object_or_404(User, id=user_id)
    paginator = get_followings_paginator(user=user)

    page = request.GET.get('page')
    try:
        following_users = paginator.page(page)
    except (EmptyPage, PageNotAnInteger):
        return HttpResponse('')

    context = {
        'user': user,
        'page': int(page),  # for page_number == page
        'following_users': following_users,
    }
    template_name = 'account/profile/followings/followingContent/followingContent.html'
    return render(request, template_name, context)

