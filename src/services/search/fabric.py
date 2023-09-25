import abc

from services.search.search import BaseSearch


class BaseSearchFabric(abc.ABC):
    @abc.abstractmethod
    def get_searcher(self) -> BaseSearch: ...
