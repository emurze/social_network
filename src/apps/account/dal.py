from django.db import models
from django.db.models import QuerySet, Exists, OuterRef, Case, When, Value

from apps.account.services.follow.action import FollowAction


class AccountDAL(models.Manager):
    def get_users(self, excluded_user) -> QuerySet:
        return (super().get_queryset().order_by('username')
                                      .exclude(id=excluded_user.id))

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
