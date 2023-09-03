import enum

from django.conf import settings

from apps.post.features.list.mixins import AddPostQuerysetMixin


class LikeAction(enum.StrEnum):
    LIKE = 'like'
    UNLIKE = 'unlike'


class AddRepliesWithoutFirstMixin:
    def get_context_data(self, *args, **kwargs):
        user = self.object
        posts = AddPostQuerysetMixin().get_queryset().filter(user=user)

        for post in posts:
            replies = post.replies.all()

            post.replies_first = replies.first()
            post.replies_without_first = replies[1:]

        kwargs['user_posts'] = posts[:settings.START_REQUEST_POST_COUNT]
        return super().get_context_data(*args, **kwargs)


class LikeActionAccountDetailMixin:
    def get_context_data(self, *args, **kwargs):
        posts = kwargs.get('user_posts')
        my_user = self.request.user

        for post in posts:
            if post.liked_users.contains(my_user):
                post.action = LikeAction.UNLIKE
            else:
                post.action = LikeAction.LIKE

        kwargs['user_posts'] = posts
        return super().get_context_data(*args, **kwargs)