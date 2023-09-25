from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from apps.dashboard.models import Action
from apps.post.models import Post, User


class ActionList(LoginRequiredMixin, ListView):
    template_name = 'dashboard/dashboard.html'
    context_object_name = 'actions'

    def get_queryset(self):
        actions = Action.objects.select_related('user')\
                                .prefetch_related('content_object')

        return actions[:settings.DEFAULT_ACTION_COUNT]

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs |= {
            'menu_selected': 'dashboard',
            'posts_count': Post.objects.count(),
            'users_count': User.objects.count(),
            'actions_count': Action.objects.count(),
        }
        return super().get_context_data(**kwargs)
