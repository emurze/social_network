from django.contrib.auth import get_user_model
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import QuerySet

from services.search.search import BaseSearch

User = get_user_model()


class UsersSearchFabric:
    @staticmethod
    def get_searcher() -> BaseSearch:
        return UsersSearch()


class UsersSearch(BaseSearch):
    def search(self, queryset: QuerySet[User], query: str) -> QuerySet:
        """Algorithm"""

        return queryset.annotate(
            similarity=TrigramSimilarity("username", query),
        ).filter(similarity__gt=0.65).order_by("similarity")
