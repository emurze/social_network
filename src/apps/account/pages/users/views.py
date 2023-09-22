import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from apps.account.pages.users.mixins import UsersListView, DefaultLimitMixin, \
    FollowActionListMixin, SearchUsersMixin, FilterUsersMixin, \
    RequestLimitMixin
from apps.account.services.follow.dispatcher import dispatch_follow_action
from services.pagination.pagination import PaginationMixin

User = get_user_model()
lg = logging.getLogger(__name__)


class AccountListView(
    DefaultLimitMixin,
    FollowActionListMixin,
    UsersListView,
):
    template_name = 'account/users/users.html'


class DownloadUsers(
    FollowActionListMixin,
    SearchUsersMixin,
    FilterUsersMixin,
    PaginationMixin,
    UsersListView
):
    template_name = 'account/users/userListGenerated/userListGenerated.html'
    paginate_by = settings.REQUEST_USER_COUNT


class SearchUsers(
    RequestLimitMixin,
    FollowActionListMixin,
    SearchUsersMixin,
    UsersListView
):
    template_name = 'account/users/userListGenerated/userListGenerated.html'


class FilterUsers(
    RequestLimitMixin,
    FollowActionListMixin,
    FilterUsersMixin,
    UsersListView
):
    template_name = 'account/users/userListGenerated/userListGenerated.html'


@login_required
@require_POST
def follow_user(request: WSGIRequest) -> JsonResponse:
    action = dispatch_follow_action(
        action=request.POST.get('action'),
        my_user=request.user,
        other_user=get_object_or_404(
            User, username=request.POST.get('username')
        )
    )
    return JsonResponse({'action': action})
