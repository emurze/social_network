from django.db import models
from django.db.models import QuerySet, Exists, OuterRef, Case, When, Value

from apps.account.services.follow.action import FollowAction


class AccountDAL(models.Manager):
    @staticmethod
    def get_users(users: QuerySet, excluded_user) -> QuerySet:
        return (
            users.exclude(id=excluded_user.id)
        )

    @staticmethod
    def annotate_follow_action(users: QuerySet, my_user):
        followed = Exists(
            my_user.followings.filter(id=OuterRef('id'))
        )
        return users.annotate(
            action=Case(
                When(followed, then=Value(FollowAction.UNFOLLOW)),
                default=Value(FollowAction.FOLLOW)
            )
        )
