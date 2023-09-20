import abc

from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import QuerySet

from apps.post.models import Post


class BaseSearchQuerySet(abc.ABC):
    @abc.abstractmethod
    def search(self, queryset: QuerySet, query: str) -> QuerySet: ...


class PostsSearchQuerySet(BaseSearchQuerySet):
    def search(self, queryset: QuerySet[Post], query: str) -> QuerySet[Post]:
        """Algorithm"""

        return queryset.annotate(
            similarity=TrigramSimilarity("description", query),
        ).filter(similarity__gt=0.65).order_by("similarity")
