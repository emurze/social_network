import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.views.generic import ListView

from apps.account.services.filter_users.filter import UsersFilterFactory
from apps.account.services.search_users.search_users import UsersSearch

User = get_user_model()
lg = logging.getLogger(__name__)


class UsersMenuSelectedMixin:
    def get_context_data(self, **kwargs):
        kwargs['menu_selected'] = 'users'
        return super().get_context_data(**kwargs)


class FollowActionListMixin:
    def get_queryset(self):
        queryset = super().get_queryset()

        users = User.ext_objects.annotate_follow_action(
            users=queryset,
            my_user=self.request.user
        )
        return users


class ListUsersMixin:
    def get_queryset(self) -> QuerySet[User]:
        users = User.ext_objects.get_users(
            excluded_user=self.request.user
        )
        return users


class UsersListView(
    LoginRequiredMixin,
    ListUsersMixin,
    ListView
):
    context_object_name = 'users'
    model = User


class BaseLimitMixin:
    limit: int

    def get_queryset(self):
        return super().get_queryset()[:self.limit]


class DefaultLimitMixin(BaseLimitMixin):
    limit: int = settings.DEFAULT_USER_COUNT


class RequestLimitMixin(BaseLimitMixin):
    limit: int = settings.REQUEST_USER_COUNT


class SearchUsersMixin:
    query: str = ''

    def get_queryset(self):
        queryset = super().get_queryset()

        self.query = self.request.GET.get('query')
        if self.query:
            searcher = UsersSearch()
            queryset = searcher.search(queryset=queryset, query=self.query)
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['query'] = self.query
        return super().get_context_data(**kwargs)


class FilterUsersMixin:
    def get_queryset(self):
        queryset = super().get_queryset()

        users_filter = UsersFilterFactory.get_filter()
        users = users_filter.filter(
            queryset=queryset,
            get=self.request.GET
        )
        return users
