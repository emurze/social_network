import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import ListView

from apps.account.services.follow.action import FollowAction
from apps.account.services.follow.dispatcher import dispatch_follow_action
from apps.account.services.follow.mixins import FollowActionListMixin
from apps.account.services.gender_age_filter.gender_age_filter import \
    gender_age_users_filter
from apps.account.services.page_downloader.page_downloader import \
    PageQuerySetDownloader
from apps.account.services.search_queryset.search_queryset import \
    BaseSearchQuerySet, UsersSearchQuerySet
from config.settings import DEFAULT_USER_COUNT

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
        return User.ext_objects.get_users(
            excluded_user=self.request.user
        )[:settings.DEFAULT_USER_COUNT]


@login_required
@require_GET
def download_users(request: WSGIRequest) -> HttpResponse:
    lg.debug(request.GET)

    users = User.ext_objects.get_users(excluded_user=request.user)
    gender_list = request.GET.getlist('gender')
    age_list = request.GET.getlist('age')
    query = request.GET.get('query')

    if query:
        searcher: BaseSearchQuerySet = UsersSearchQuerySet(
            queryset=users,
            query=query,
        )
        users = searcher.search()

        lg.debug('QUERY WORKED')

    if gender_list or age_list:
        users = gender_age_users_filter(
            users=users,
            gender_list=gender_list,
            age_list=age_list,
        )

        lg.debug('FILTERS WORKED')

    downloader = PageQuerySetDownloader(
        request=request,
        page=request.GET.get('page'),
        queryset=users,
        per_page_count=settings.REQUEST_USER_COUNT,
        context_object_name='users',
        template_name='account/users/userListGenerated/userListGenerated.html',
        mixins=(FollowActionListMixin,),
    )

    return downloader.render()


@login_required
@require_GET
def search_users(request: WSGIRequest) -> HttpResponse:
    query = request.GET.get('query')
    searcher: BaseSearchQuerySet = UsersSearchQuerySet(
        queryset=User.objects.exclude(id=request.user.id),
        query=query,
    )
    users = searcher.search()

    my_user = request.user
    for user in users:
        if my_user.followings.contains(user):
            user.action = FollowAction.UNFOLLOW
        else:
            user.action = FollowAction.FOLLOW

    context = {
        'users': users[:DEFAULT_USER_COUNT],
        'query': query,
    }
    template_name = 'account/users/userListGenerated/userListGenerated.html'
    return render(request, template_name, context)


@login_required
@require_GET
def filter_users(request: WSGIRequest) -> HttpResponse:
    users = User.ext_objects.get_users(excluded_user=request.user)
    users = gender_age_users_filter(
        users=users,
        gender_list=request.GET.getlist('gender'),
        age_list=request.GET.getlist('age'),
    )

    lg.debug(users)

    my_user = request.user
    for user in users:
        if my_user.followings.contains(user):
            user.action = FollowAction.UNFOLLOW
        else:
            user.action = FollowAction.FOLLOW

    template_name = 'account/users/userListGenerated/userListGenerated.html'
    context = {
        'users': users[:settings.DEFAULT_USER_COUNT],
    }
    return render(request, template_name, context)
