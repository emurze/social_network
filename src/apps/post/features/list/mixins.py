from django.conf import settings
from django.db.models import Count, QuerySet

from apps.post.features.create.forms import PostForm
from apps.post.features.list.forms import ReplyForm
from apps.post.models import Post


class AddReplyFormMixin:
    def get_context_data(self, *args, **kwargs):
        kwargs['reply_form'] = ReplyForm()
        return super().get_context_data(*args, **kwargs)


class AddPostForm:
    def get_context_data(self, *args, **kwargs):
        kwargs['post_form'] = PostForm()
        return super().get_context_data(*args, **kwargs)


class AddPostQuerysetMixin:
    def get_queryset(self) -> QuerySet[Post]:
        posts = Post.objects.annotate(
            likes_count=Count('liked_users', distinct=True),
            reply_count=Count('replies', distinct=True)
        ).order_by('-created').select_related(
            'user'
        ).prefetch_related('replies', 'replies__user', 'liked_users')
        return posts


class PageLimitQuerysetMixin:
    def get_queryset(self) -> QuerySet[Post]:
        """Limit queryset as one page"""
        return super().get_queryset()[:settings.START_REQUEST_POST_COUNT]
