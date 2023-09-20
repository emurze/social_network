import abc

from django.contrib.auth import get_user_model
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import QuerySet

User = get_user_model()


class BaseSearchQuerySet(abc.ABC):
    @abc.abstractmethod
    def search(self, queryset: QuerySet, query: str) -> QuerySet: ...


class UsersSearchQuerySet(BaseSearchQuerySet):
    def search(self, queryset: QuerySet[User], query: str) -> QuerySet:
        """Algorithm"""

        return queryset.annotate(
            similarity=TrigramSimilarity("username", query),
        ).filter(similarity__gt=0.65).order_by("similarity")
