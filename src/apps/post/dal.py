from django.db import models
from django.db.models import Count


class PostDAL(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-created').annotate(
            likes_count=Count('liked_users', distinct=True),
            reply_count=Count('replies', distinct=True)
        ).select_related('user')\
            .prefetch_related('replies', 'replies__user', 'liked_users')
