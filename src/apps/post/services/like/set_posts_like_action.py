from django.contrib.auth import get_user_model
from django.db.models import QuerySet, Case, When, F, Exists, OuterRef

from apps.post.models import Post
from apps.post.services.like.action import LikeAction

User = get_user_model()


def set_posts_like_action(posts: QuerySet[Post], my_user: User):
    for post in posts:
        if post.liked_users.contains(my_user):
            post.action = LikeAction.UNLIKE
        else:
            post.action = LikeAction.LIKE

    # liked = Exists(
    #     User.objects.filter(
    #         id=my_user.id,
    #         liked_posts__in=[OuterRef('id')],
    #     )
    # )
    # posts = posts.annotate(
    #     action=Case(
    #         When(liked, then=LikeAction.UNLIKE))
    # )

    return posts
