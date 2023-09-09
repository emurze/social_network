import logging

from django.conf import settings

from apps.account.features.detail.forms import EditCoverForm
from apps.account.features.detail.services.get_followings_paginator import \
    get_followings_paginator
from apps.post.features.list.mixins import AddPostQuerysetMixin
from apps.post.services.like.action import LikeAction

lg = logging.getLogger(__name__)


class AddUserPosts:
    def get_context_data(self, *args, **kwargs):
        user = self.object
        posts = AddPostQuerysetMixin().get_queryset().filter(user=user)
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

        paginator = get_followings_paginator(user=user)
        following_users = paginator.page(
            settings.DEFAULT_SHOWED_FOLLOWINGS_PAGE
        )

        kwargs['following_users'] = following_users
        kwargs['page'] = settings.DEFAULT_SHOWED_FOLLOWINGS_PAGE

        return super().get_context_data(*args, **kwargs)
