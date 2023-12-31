import logging

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Count, Exists, OuterRef, QuerySet, Case, When, \
    Value, Prefetch

from apps.post.services.like.action import LikeAction

User = get_user_model()
lg = logging.getLogger(__name__)


class PostDAL(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-created').annotate(
            likes_count=Count('liked_users', distinct=True),
            reply_count=Count('replies', distinct=True)
        )

    @staticmethod
    def annotate_like_action(posts: QuerySet, my_user: User):
        liked = Exists(
            my_user.liked_posts.filter(id=OuterRef('id'))
        )
        posts = posts.annotate(
            action=Case(
                When(liked, then=Value(LikeAction.UNLIKE)),
                default=Value(LikeAction.LIKE)
            )
        )
        return posts
