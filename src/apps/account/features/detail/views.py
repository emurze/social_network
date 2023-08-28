import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import DetailView

from apps.account.mixins import ProfileSelectedMixin

User = get_user_model()
lg = logging.getLogger(__name__)


class FollowActionMixin:
    def get_context_data(self, *args, **kwargs):
        user = self.object
        your_user = self.request.user

        if your_user.followers.contains(user):
            action = 'unfollow'
        else:
            action = 'follow'

        kwargs['action'] = action
        return super().get_context_data(*args, **kwargs)


@login_required
@require_POST
def follow_view(request: WSGIRequest, username: str) -> JsonResponse:
    user = get_object_or_404(User, username=username)
    my_user = request.user

    action = request.POST.get('action')
    match action:
        case 'follow':
            action = 'unfollow'
            my_user.followings.add(user)

        case 'unfollow':
            action = 'follow'
            my_user.followings.remove(user)

    return JsonResponse({'action': action})


class AccountDetailView(
    LoginRequiredMixin,
    ProfileSelectedMixin,
    FollowActionMixin,
    DetailView
):
    model = User
    template_name = 'account/profile/profile.html'
    context_object_name = 'user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
