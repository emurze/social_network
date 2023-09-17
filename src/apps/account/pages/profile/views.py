import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import DetailView, UpdateView

from .forms import EditCoverForm, AccountEditForm
from .mixins import AddUserPosts, LikeActionAccountDetailMixin, \
    AddFollowingUsersMixin, ProfileSelectedMixin, AjaxErrorsMixin

from apps.account.services.follow.dispatcher import dispatch_follow_action
from apps.account.services.follow.mixins import FollowActionDetailMixin
from apps.account.services.page_downloader.page_downloader import \
    PageQuerySetDownloader
from apps.post.pages.posts.mixins import AddReplyFormMixin, AddPostForm

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


class AccountEditView(LoginRequiredMixin, AjaxErrorsMixin, UpdateView):
    model = User
    form_class = AccountEditForm
    template_name = 'account/profile/edit_window/edit_window.html'
    context_object_name = 'user'
    slug_field = 'username'
    slug_url_kwarg = 'username'


@login_required
@require_GET
def follow_pagination(request: WSGIRequest, user_id: int) -> HttpResponse:
    user = get_object_or_404(User, id=user_id)
    page = request.GET.get('page')

    downloader = PageQuerySetDownloader(
        request=request,
        page=page,
        queryset=user.get_followings(),
        per_page_count=settings.REQUEST_FOLLOWINGS_COUNT,
        context_object_name='following_users',
        template_name='account/profile/followings/followingContent/'
                      'followingContent.html',
        extra_context={
            'user': user,
            'page': int(page)
        },
    )
    return downloader.render()


@login_required
@require_POST
def edit_cover(request: WSGIRequest, username: str) -> HttpResponse:
    user = get_object_or_404(User, username=username)
    form = EditCoverForm(
        instance=user,
        data=request.POST,
        files=request.FILES,
    )

    if form.is_valid():
        form.save()
    else:
        lg.warning('User edit form without data.')

    return HttpResponse('')
