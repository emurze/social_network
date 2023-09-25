import abc

from django.db.models import QuerySet


class BaseSearch(abc.ABC):
    @abc.abstractmethod
    def search(self, queryset: QuerySet, query: str) -> QuerySet: ...
