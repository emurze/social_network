import itertools

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

User = get_user_model()
AGE_DICT = {
    'Y': (10, 18),
    'YA': (18, 26),
    'A': (26, 34),
    'PA': (34, settings.OLDEST_HUMAN),
}


def gender_age_users_filter(
    gender_list: list[str],
    age_list: list[str],
    users: QuerySet[User],
) -> QuerySet[User]:

    age_gen = (age for x in age_list if (age := AGE_DICT.get(x)))

    options = {}
    if gender_list:
        options['gender__in'] = gender_list
    if age_list:
        range_set = itertools.starmap(range, age_gen)
        age_range = set(itertools.chain(*range_set))
        birthday_range = [settings.CURRENT_YEAR - age for age in age_range]
        options['birthday__year__in'] = birthday_range

    return users.filter(**options)
