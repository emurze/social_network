import abc
from typing import Any

from django.db.models import QuerySet


class BaseSpecification(abc.ABC):
    db_field_name: str
    data: Any

    @abc.abstractmethod
    def filter(self, queryset: QuerySet) -> QuerySet: ...
