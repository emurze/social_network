import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import ListView

from apps.account.services.follow.dispatcher import dispatch_follow_action
from apps.account.services.follow.mixins import FollowActionListMixin
from apps.account.services.page_downloader.page_downloader import \
    PageQuerySetDownloader

User = get_user_model()
lg = logging.getLogger(__name__)


@login_required
@require_POST
def follow_list(request: WSGIRequest) -> JsonResponse:
    username = request.POST.get('username')

    action = dispatch_follow_action(
        action=request.POST.get('action'),
        my_user=request.user,
        other_user=get_object_or_404(User, username=username)
    )
    return JsonResponse({'action': action})


class AccountListView(LoginRequiredMixin, FollowActionListMixin, ListView):
    template_name = 'account/users/users.html'
    context_object_name = 'users'

    def get_queryset(self) -> QuerySet[User]:
        ordered_users = User.objects.order_by('username')
        filtered_users = ordered_users.exclude(id=self.request.user.id)

        return filtered_users[:settings.DEFAULT_USER_COUNT]


@login_required
@require_GET
def download_users(request: WSGIRequest) -> HttpResponse:
    downloader = PageQuerySetDownloader(
        request=request,
        page=request.GET.get('page'),
        queryset=User.objects.all(),
        per_page_count=settings.REQUEST_USER_COUNT,
        context_object_name='users',
        template_name='account/users/userListGenerated/userListGenerated.html',
        mixins=(FollowActionListMixin,),
    )
    return downloader.render()
