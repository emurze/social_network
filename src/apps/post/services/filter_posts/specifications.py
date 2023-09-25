import enum
import logging
from dataclasses import dataclass

from django.db.models import QuerySet
from django.http import QueryDict

from apps.post.models import Post
from services.filter import BaseSpecCollection, BaseSpecification

lg = logging.getLogger(__name__)


class Order(enum.StrEnum):
    DESC = 'DESC'
    ASC = 'ASC'


class PostsSpecCollection(BaseSpecCollection):
    @staticmethod
    def get_specifications(get: QueryDict):
        order = get.get('order', '')
        verified = bool(get.get('verified', False))
        photo = bool(get.get('photo', False))

        return (
            OrderPostsSpecification(data=order),
            PhotoPostsSpecification(data=photo),
            VerifiedPostsSpecification(data=verified),
        )


@dataclass
class OrderPostsSpecification(BaseSpecification):
    db_field_name: str = 'created'
    data: str = ''

    def filter(self, queryset: QuerySet[Post]) -> QuerySet[Post]:
        if self.data == Order.DESC:
            sign = '-'
        else:
            sign = ''
        return queryset.order_by(f'{sign}{self.db_field_name}')


@dataclass
class PhotoPostsSpecification(BaseSpecification):
    db_field_name: str = 'photo'
    data: bool = False

    def filter(self, queryset: QuerySet[Post]) -> QuerySet[Post]:
        return queryset.exclude(**{self.db_field_name: ''})


@dataclass
class VerifiedPostsSpecification(BaseSpecification):
    db_field_name: str = 'user__is_staff'
    data: bool = False

    def filter(self, queryset: QuerySet[Post]) -> QuerySet[Post]:
        return queryset.filter(**{self.db_field_name: self.data})
