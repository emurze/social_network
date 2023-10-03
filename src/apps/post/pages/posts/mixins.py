import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.views.generic import ListView

from .forms import PostForm, ReplyForm
from ...models import Post
from ...services.filter_posts.filters import PostsFiltersFactory
from ...services.search_posts.search_posts import PostsSearchFactory

lg = logging.getLogger(__name__)
User = get_user_model()


class PostsMenuSelectedMixin:
    def get_context_data(self, **kwargs):
        kwargs['menu_selected'] = 'posts'
        return super().get_context_data(**kwargs)


class AddReplyFormMixin:
    def get_context_data(self, *args, **kwargs) -> dict:
        kwargs['reply_form'] = ReplyForm()
        return super().get_context_data(*args, **kwargs)


class AddPostForm:
    def get_context_data(self, *args, **kwargs) -> dict:
        kwargs['post_form'] = PostForm()
        return super().get_context_data(*args, **kwargs)


class LikeActionListMixin:
    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()

        return Post.ext_objects.annotate_like_action(
            posts=queryset,
            my_user=self.request.user
        )


class SearchPostsMixin:
    query = ''

    @staticmethod
    def search(queryset: QuerySet, query: str) -> QuerySet:
        searcher = PostsSearchFactory.get_searcher()
        queryset = searcher.search(
            queryset=queryset,
            query=query,
        )
        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()

        self.query = self.request.GET.get('query')
        if self.query:
            queryset = self.search(queryset, self.query)

        return queryset

    def get_context_data(self, **kwargs):
        kwargs['query'] = self.query
        return super().get_context_data(**kwargs)


class FilterPostsMixin:
    @staticmethod
    def filter(queryset: QuerySet, get) -> QuerySet:
        posts_filter = PostsFiltersFactory.get_filter()
        posts = posts_filter.filter(
            queryset=queryset,
            get=get
        )
        return posts

    def get_queryset(self):
        queryset = super().get_queryset()
        posts = self.filter(
            queryset=queryset,
            get=self.request.GET
        )
        return posts


class FilterOwnerMixin:
    @staticmethod
    def filter_by_owner(queryset: QuerySet, owner_id: int) -> QuerySet:
        return queryset.filter(user_id=owner_id)

    def get_queryset(self):
        queryset = super().get_queryset()

        if owner_id := self.request.GET.get('owner_id'):
            self.filter_by_owner(queryset, owner_id)

        return queryset


class BaseLimitPostsMixin:
    limit: int

    def get_queryset(self):
        return super().get_queryset()[:self.limit]


class DefaultLimitPostsMixin(BaseLimitPostsMixin):
    limit = settings.DEFAULT_POST_COUNT


class RequestLimitPostsMixin(BaseLimitPostsMixin):
    limit = settings.DEFAULT_POST_COUNT


class PostListViewMixin(
    LoginRequiredMixin,
    AddReplyFormMixin,
    AddPostForm,
    ListView,
):
    queryset = Post.ext_objects.all()
    context_object_name = 'posts'

    def get_context_data(self, *args, **kwargs) -> dict:
        kwargs['user'] = None
        return super().get_context_data(**kwargs)
