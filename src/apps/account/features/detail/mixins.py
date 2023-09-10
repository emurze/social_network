import logging

from django.conf import settings
from django.core.paginator import Paginator

from apps.post.models import Post
from apps.post.services.like.action import LikeAction

lg = logging.getLogger(__name__)


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
