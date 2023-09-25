from apps.account.services.filter_users.specification import \
    UsersSpecCollection
from services.filter import BaseFilterFactory, DefaultFilter, BaseFilter


class UsersFilterFactory(BaseFilterFactory):
    @staticmethod
    def get_filter() -> BaseFilter:
        return UsersFilter()


class UsersFilter(DefaultFilter):
    spec_collection_class = UsersSpecCollection
