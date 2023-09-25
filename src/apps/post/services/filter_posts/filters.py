from apps.post.services.filter_posts.specifications import PostsSpecCollection
from services.filter import BaseFilterFactory, BaseFilter
from services.filter import DefaultFilter


class PostsFiltersFactory(BaseFilterFactory):
    @staticmethod
    def get_filter() -> BaseFilter:
        return PostsFilter()


class PostsFilter(DefaultFilter):
    spec_collection_class = PostsSpecCollection
