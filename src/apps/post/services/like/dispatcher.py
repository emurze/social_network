from django.contrib.auth import get_user_model

from apps.dashboard.services.create_action import create_action
from apps.post.models import Post
from .action import LikeAction

User = get_user_model()


def dispatch_like_action(action: LikeAction, post: Post,
                         my_user: User) -> LikeAction:
    match action:
        case LikeAction.LIKE:
            post.liked_users.add(my_user)
            action = LikeAction.UNLIKE
            create_action(my_user, 'likes post', post)

        case LikeAction.UNLIKE:
            post.liked_users.remove(my_user)
            action = LikeAction.LIKE

    return action
