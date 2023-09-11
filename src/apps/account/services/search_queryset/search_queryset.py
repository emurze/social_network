import abc
from dataclasses import dataclass, field

from django.db.models import QuerySet


class BaseSearchQuerySet(abc.ABC):
    @abc.abstractmethod
    def get_queryset(self) -> QuerySet: ...
    @abc.abstractmethod
    def get_query(self) -> str: ...
    @abc.abstractmethod
    def search(self) -> QuerySet: ...


@dataclass
class SearchQuerySet(BaseSearchQuerySet):
    queryset: QuerySet = field(repr=False)
    query: str

    def search(self) -> QuerySet:
        """Algorithm"""
        return self.queryset

    def get_queryset(self) -> QuerySet:
        return self.queryset

    def get_query(self) -> str:
        return self.query
