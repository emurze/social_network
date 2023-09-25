import itertools
from dataclasses import field, dataclass

from django.conf import settings
from django.db.models import QuerySet
from django.http import QueryDict

from apps.post.models import User
from services.filter import BaseSpecCollection, BaseSpecification

AGE_DICT = {
    'Y': (10, 18),
    'YA': (18, 26),
    'A': (26, 34),
    'PA': (34, settings.OLDEST_HUMAN),
}


class UsersSpecCollection(BaseSpecCollection):
    @staticmethod
    def get_specifications(get: QueryDict) -> tuple[BaseSpecification, ...]:
        gender_list = get.getlist('gender')
        age_list = get.getlist('age')

        return (
            GenderSpecification(data=gender_list),
            AgeSpecification(data=age_list),
        )


@dataclass
class GenderSpecification(BaseSpecification):
    db_field_name = 'gender__in'
    data: list[str] = field(default_factory=list)

    def filter(self, queryset: QuerySet[User]) -> QuerySet[User]:
        return queryset.filter(**{self.db_field_name: self.data})


@dataclass
class AgeSpecification(BaseSpecification):
    db_field_name = 'birthday__year__in'
    data: list[str] = field(default_factory=list)

    def filter(self, queryset: QuerySet[User]) -> QuerySet[User]:
        age_gen = (age for x in self.data if (age := AGE_DICT.get(x)))
        range_set = itertools.starmap(range, age_gen)

        age_range = set(itertools.chain(*range_set))
        birthday_range = [settings.CURRENT_YEAR - age for age in age_range]

        return queryset.filter(**{self.db_field_name: birthday_range})
