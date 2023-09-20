import logging
from typing import Any

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse

from .forms import AccountEditForm

from apps.post.models import Post
from apps.post.services.like.action import LikeAction
from ...services.follow.action import FollowAction

lg = logging.getLogger(__name__)
User = get_user_model()


class AddUserPosts:
    def get_context_data(self, *args, **kwargs):
        user = self.object
        posts = Post.objects.all().filter(user=user)
        kwargs['user_posts'] = posts[:settings.START_REQUEST_POST_COUNT]
        kwargs['is_user_posts'] = True
        return super().get_context_data(*args, **kwargs)


class LikeActionAccountDetailMixin:
    def get_context_data(self, *args, **kwargs):
        posts = kwargs.get('user_posts')
        my_user = self.request.user

        # QUERY OPTIMIZATION

        # posts = posts.annotate(action=F('liked_users'))

        for post in posts:
            if post.liked_users.contains(my_user):
                post.action = LikeAction.UNLIKE
            else:
                post.action = LikeAction.LIKE

        kwargs['user_posts'] = posts
        return super().get_context_data(*args, **kwargs)


class AddFollowingUsersMixin:
    def get_context_data(self, *args, **kwargs):
        user = self.object

        paginator = Paginator(
            user.get_followings(),
            settings.DEFAULT_FOLLOWINGS_COUNT
        )
        following_users = paginator.page(
            settings.DEFAULT_SHOWED_FOLLOWINGS_PAGE
        )

        kwargs['following_users'] = following_users
        kwargs['page'] = settings.DEFAULT_SHOWED_FOLLOWINGS_PAGE

        return super().get_context_data(*args, **kwargs)


class ProfileSelectedMixin:
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        user = self.object
        if self.request.user == user:
            kwargs['icon_menu__selected'] = 'profile'
            kwargs['is_owner'] = True
        return super().get_context_data(**kwargs)


class AjaxErrorsMixin:
    @staticmethod
    def form_invalid(form: AccountEditForm) -> HttpResponse:
        form._errors['is_errors'] = True
        return JsonResponse(form._errors)


class FollowActionDetailMixin:
    @staticmethod
    def _set_follow_action(requested_user: User, user: User) -> LikeAction:
        if requested_user.followings.contains(user):
            action = FollowAction.UNFOLLOW
        else:
            action = FollowAction.FOLLOW
        return action

    def get_context_data(self, *args, **kwargs):
        action = self._set_follow_action(
            requested_user=self.request.user,
            user=self.object,
        )

        kwargs['action'] = action
        return super().get_context_data(*args, **kwargs)
