from django.conf import settings

from apps.post.features.list.mixins import AddPostQuerysetMixin
from apps.post.services.like.action import LikeAction


class AddUserPosts:
    def get_context_data(self, *args, **kwargs):
        user = self.object
        posts = AddPostQuerysetMixin().get_queryset().filter(user=user)
        kwargs['user_posts'] = posts[:settings.START_REQUEST_POST_COUNT]
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
