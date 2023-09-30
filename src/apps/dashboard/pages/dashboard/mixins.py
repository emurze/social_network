import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from apps.dashboard.models import Action
from apps.post.models import Post
from services.queryset_chain.queryset_chain import QuerySetChain

User = get_user_model()
lg = logging.getLogger(__name__)


class ActionMenuSelectedMixin:
    def get_context_data(self, **kwargs) -> dict:
        kwargs['menu_selected'] = 'dashboard'
        return super().get_context_data(**kwargs)


class ActionCountersMixin:
    def get_context_data(self, **kwargs) -> dict:
        kwargs |= {
            'posts_count': Post.objects.count(),
            'users_count': User.objects.count(),
            'actions_count': Action.objects.count(),
        }
        return super().get_context_data(**kwargs)


class ActionListMixin(
    LoginRequiredMixin,
    ActionMenuSelectedMixin,
    ListView
):
    context_object_name = 'actions'
    queryset = Action.objects.select_related('user')


class ActionLimitQuerysetMixin:
    limit = settings.DEFAULT_ACTION_COUNT

    def get_queryset(self):
        return super().get_queryset()[:self.limit]
