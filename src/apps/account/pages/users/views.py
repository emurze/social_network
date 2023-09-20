import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from apps.account.pages.users.mixins import UsersListView
from apps.account.services.filter_users.filter import UsersFilterFabric
from apps.account.services.follow.dispatcher import dispatch_follow_action
from apps.account.services.search_users.search_users import UsersSearch, \
    UsersSearchFabric
from config.settings import DEFAULT_USER_COUNT

User = get_user_model()
lg = logging.getLogger(__name__)


class AccountListView(UsersListView):
    template_name = 'account/users/users.html'
    context_object_name = 'users'

    def get_queryset(self) -> QuerySet[User]:
        return User.ext_objects.get_users(
            excluded_user=self.request.user
        )[:settings.DEFAULT_USER_COUNT]


class DownloadUsers(UsersListView):
    template_name = 'account/users/userListGenerated/userListGenerated.html'
    context_object_name = 'users'
    paginate_by = settings.REQUEST_USER_COUNT

    def get_queryset(self):
        users = User.ext_objects.get_users(excluded_user=self.request.user)
        query = self.request.GET.get('query')

        if query:
            searcher = UsersSearch()
            users = searcher.search(queryset=users, query=query)

        users_filter = UsersFilterFabric.get_filter()
        users = users_filter.filter(
            queryset=users,
            get=self.request.GET
        )
        return users


class SearchUsers(UsersListView):
    template_name = 'account/users/userListGenerated/userListGenerated.html'
    context_object_name = 'users'
    query = ''

    def get_queryset(self) -> HttpResponse:
        self.query = self.request.GET.get('query')

        searcher = UsersSearchFabric.get_searcher()
        users = searcher.search(
            queryset=User.objects.exclude(id=self.request.user.id),
            query=self.query,
        )
        return users[:DEFAULT_USER_COUNT]

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs['query'] = self.query
        return super().get_context_data(**kwargs)


class FilterUsers(UsersListView):
    template_name = 'account/users/userListGenerated/userListGenerated.html'
    context_object_name = 'users'

    def get_queryset(self):
        users = User.ext_objects.get_users(
            excluded_user=self.request.user
        )
        users_filter = UsersFilterFabric.get_filter()
        users = users_filter.filter(
            queryset=users,
            get=self.request.GET
        )
        return users[:settings.DEFAULT_USER_COUNT]


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
