from apps.post.services.like.action import LikeAction


class LikeActionListMixin:
    def get_context_data(self, *args, **kwargs):
        posts = self.object_list
        my_user = self.request.user

        for post in posts:
            if post.liked_users.contains(my_user):
                post.action = LikeAction.UNLIKE
            else:
                post.action = LikeAction.LIKE

        return super().get_context_data(*args, **kwargs)
