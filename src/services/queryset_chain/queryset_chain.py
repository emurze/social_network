import abc

from django.db.models import QuerySet


class QuerySetChain(abc.ABC):
    @abc.abstractmethod
    def get_queryset(self) -> QuerySet: ...
