import abc

from django.http import QueryDict

from .specification import BaseSpecification


class BaseSpecCollection(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def get_specifications(get: QueryDict) -> tuple[BaseSpecification]: ...
