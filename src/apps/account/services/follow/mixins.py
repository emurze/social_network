from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from apps.account.services.follow.action import FollowAction
from apps.post.services.like.action import LikeAction

User = get_user_model()


class FollowActionDetailMixin:
    @staticmethod
    def _set_follow_action(requested_user: User, user: User) -> LikeAction:
        if requested_user.followings.contains(user):
            action = FollowAction.UNFOLLOW
        else:
            action = FollowAction.FOLLOW
        return action

    def get_context_data(self, *args, **kwargs):
        user = self.object
        my_user = self.request.user

        action = self._set_follow_action(
            requested_user=self.request.user,
            user=self.object,
        )

        kwargs['action'] = action
        return super().get_context_data(*args, **kwargs)


class FollowActionListMixin:
    @staticmethod
    def set_follow_actions(requested_user: User,
                           users: QuerySet[User]) -> QuerySet[User]:
        for user in users:
            if requested_user.followings.contains(user):
                user.action = FollowAction.UNFOLLOW
            else:
                user.action = FollowAction.FOLLOW
        return users

    def get_context_data(self, *args, **kwargs):
        self.set_follow_actions(
            requested_user=self.request.user,
            users=self.object_list
        )

        return super().get_context_data(*args, **kwargs)
