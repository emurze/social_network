from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import QuerySet

from apps.post.models import Post
from services.search import BaseSearch


class PostsSearchFactory:
    @staticmethod
    def get_searcher() -> BaseSearch:
        return PostsSearch()


class PostsSearch(BaseSearch):
    def search(self, queryset: QuerySet[Post], query: str) -> QuerySet[Post]:
        """Algorithm"""

        return queryset.annotate(
            similarity=TrigramSimilarity("description", query),
        ).filter(similarity__gt=0.1).order_by("similarity")
