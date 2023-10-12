from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

from apps.account.services.follow.action import FollowAction
from apps.post.models import Post
from apps.post.pages.posts.views import PostsQuery

User = get_user_model()


class ProfileSelectedMixin:
    def get_context_data(self, **kwargs) -> dict:
        user = self.object
        if self.request.user == user:
            kwargs['icon_menu__selected'] = 'profile'
            kwargs['is_owner'] = True
        return super().get_context_data(**kwargs)


class AddFollowActionMixin:
    @staticmethod
    def _set_follow_action(requested_user: User, user: User) -> FollowAction:
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


class AddFollowingUsersMixin:
    def get_context_data(self, *args, **kwargs):
        user = self.object
        followings = user.get_followings()\
                         .only(
                            'photo',
                            'gender',
                            'is_staff',
                            'username',
                        )

        paginator = Paginator(
            followings,
            settings.DEFAULT_FOLLOWINGS_COUNT
        )
        following_users = paginator.page(
            settings.DEFAULT_SHOWED_FOLLOWINGS_PAGE
        )

        kwargs['exists_followings_users'] = followings.exists()
        kwargs['following_users'] = following_users
        kwargs['page'] = settings.DEFAULT_SHOWED_FOLLOWINGS_PAGE

        return super().get_context_data(*args, **kwargs)


class AddUserPosts:
    def get_context_data(self, *args, **kwargs):
        user = self.object
        my_user = self.request.user

        posts = PostsQuery.queryset.filter(user_id=user.id)
        posts = Post.ext_objects.annotate_like_action(posts, my_user)

        kwargs['user_posts'] = posts[:settings.DEFAULT_POST_COUNT]
        kwargs['is_user_posts'] = True

        return super().get_context_data(*args, **kwargs)
