from django.db import models
from django.db.models import QuerySet


class AccountDAL(models.Manager):
    def get_users(self, excluded_user) -> QuerySet:
        return (super().get_queryset().order_by('username')
                                      .exclude(id=excluded_user.id))
