import itertools
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
from apps.account.services.page_downloader.page_downloader import \
    PageQuerySetDownloader
from apps.account.services.search_queryset.search_queryset import \
    BaseSearchQuerySet, SearchQuerySet

User = get_user_model()
lg = logging.getLogger(__name__)
AGE_DICT = {
    'Y': (10, 18),
    'YA': (18, 26),
    'A': (26, 34),
    'PA': (34, settings.OLDEST_HUMAN),
}


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
    lg.debug(f'DOWNLOAD {request.GET}')

    users = User.objects.all()

    gender_list = request.GET.getlist('gender')
    requested_age_list = request.GET.getlist('age')
    age_list = (age for x in requested_age_list if (age := AGE_DICT.get(x)))

    options = {}
    if gender_list:
        options['gender__in'] = gender_list
    if requested_age_list:
        range_set = itertools.starmap(range, age_list)
        age_range = set(itertools.chain(*range_set))
        birthday_range = [settings.CURRENT_YEAR - age for age in age_range]
        options['birthday__year__in'] = birthday_range

    lg.debug(f'OPTIONS {options}')
    users = users.filter(**options)

    lg.debug(f'USERS 2 {users}')

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

    searcher: BaseSearchQuerySet = SearchQuerySet(
        queryset=User.objects.all(),
        query=query,
    )
    lg.debug(searcher)
    lg.debug('test')

    return HttpResponse('')


@login_required
@require_GET
def filter_users(request: WSGIRequest) -> HttpResponse:
    lg.debug(f'FILTER {request.GET}')

    gender_list = request.GET.getlist('gender')
    requested_age_list = request.GET.getlist('age')

    age_list = (age for x in requested_age_list if (age := AGE_DICT.get(x)))
    users = User.ext_objects.get_users(excluded_user=request.user)

    options = {}
    if gender_list:
        options['gender__in'] = gender_list
    if requested_age_list:
        range_set = itertools.starmap(range, age_list)
        age_range = set(itertools.chain(*range_set))
        birthday_range = [settings.CURRENT_YEAR - age for age in age_range]
        options['birthday__year__in'] = birthday_range

    users = users.filter(**options)

    my_user = request.user
    for user in users:
        if my_user.followings.contains(user):
            user.action = FollowAction.UNFOLLOW
        else:
            user.action = FollowAction.FOLLOW

    template_name = 'account/users/userListGenerated/userListGenerated.html'
    context = {'users': users[:settings.DEFAULT_USER_COUNT]}
    return render(request, template_name, context)
