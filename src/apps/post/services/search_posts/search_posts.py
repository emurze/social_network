from dataclasses import dataclass, field

from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import QuerySet

from apps.account.services.search_queryset.search_queryset import \
    BaseSearchQuerySet


@dataclass
class PostsSearchQuerySet(BaseSearchQuerySet):
    queryset: QuerySet = field(repr=False)
    query: str

    def search(self) -> QuerySet:
        """Algorithm"""

        return self.queryset.annotate(
            similarity=TrigramSimilarity("description", self.query),
        ).filter(similarity__gt=0.65).order_by("similarity")

    def get_queryset(self) -> QuerySet:
        return self.queryset

    def get_query(self) -> str:
        return self.query
