import abc

from .filter import BaseFilter


class BaseFilterFactory(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def get_filter() -> BaseFilter: ...
