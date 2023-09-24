from django.contrib.auth import get_user_model

from apps.account.services.follow.action import FollowAction
from apps.dashboard.services.create_action import create_action

User = get_user_model()


def dispatch_follow_action(
    action: FollowAction,
    my_user: User,
    other_user: User
) -> FollowAction:
    """
    Un | Follows your user to another user.
    Returns prepared action.
    """

    match action:
        case FollowAction.FOLLOW:
            action = FollowAction.UNFOLLOW
            my_user.followings.add(other_user)
            create_action(my_user, 'follows user', other_user)

        case FollowAction.UNFOLLOW:
            action = FollowAction.FOLLOW
            my_user.followings.remove(other_user)

    return action
