from apps.account.sevices.follow.action import FollowAction


class FollowActionDetailMixin:
    def get_context_data(self, *args, **kwargs):
        user = self.object
        my_user = self.request.user

        if my_user.followings.contains(user):
            action = FollowAction.UNFOLLOW
        else:
            action = FollowAction.FOLLOW

        kwargs['action'] = action
        return super().get_context_data(*args, **kwargs)


class FollowActionListMixin:
    def get_context_data(self, *args, **kwargs):
        users = self.object_list
        my_user = self.request.user

        # users.annotate(When())

        for user in users:
            if my_user.followings.contains(user):
                user.action = FollowAction.UNFOLLOW
            else:
                user.action = FollowAction.FOLLOW

        return super().get_context_data(*args, **kwargs)
