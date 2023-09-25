import abc
from django.db.models import QuerySet
from django.http import QueryDict

from apps.post.models import Post
from .spec_collection import BaseSpecCollection
from .exceptions import CollectionNotExistsError


class BaseFilter(abc.ABC):
    @abc.abstractmethod
    def filter(self, queryset: QuerySet, get: QueryDict) -> QuerySet[Post]: ...


class DefaultFilter(BaseFilter):
    spec_collection_class: BaseSpecCollection | None = None

    def filter(self, queryset: QuerySet, get: QueryDict) -> QuerySet[Post]:
        if not self.spec_collection_class:
            raise CollectionNotExistsError(
                'Please check that spec_collection_class is exists'
            )

        specs = self.spec_collection_class.get_specifications(get=get)
        for spec in specs:
            if spec.data:
                queryset = spec.filter(queryset=queryset)
        return queryset
