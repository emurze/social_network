from apps.post.services.like.action import LikeAction


def dispatch_like_action(action, post, my_user) -> LikeAction:
    match action:
        case LikeAction.LIKE:
            post.liked_users.add(my_user)
            action = LikeAction.UNLIKE

        case LikeAction.UNLIKE:
            post.liked_users.remove(my_user)
            action = LikeAction.LIKE

    return action
