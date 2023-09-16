import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import ListView
from rest_framework.generics import get_object_or_404

from apps.account.services.page_downloader.page_downloader import \
    PageQuerySetDownloader
from apps.account.services.search_queryset.search_queryset import \
    BaseSearchQuerySet
from .mixins import AddReplyFormMixin, AddPostForm

from apps.post.models import Post, Reply
from .forms import PostForm, ReplyForm
from apps.post.services.like.action import LikeAction
from apps.post.services.like.dispatcher import dispatch_like_action
from apps.post.services.like.mixins import LikeActionListMixin
from django.conf import settings

from ...services.search_posts.search_posts import PostsSearchQuerySet

lg = logging.getLogger(__name__)
SHOWED_REPLY_COUNT = 1


class PostListView(
    LoginRequiredMixin,
    AddReplyFormMixin,
    AddPostForm,
    LikeActionListMixin,
    ListView,
):
    template_name = 'post/posts/posts.html'
    queryset = Post.objects.all()[:settings.START_REQUEST_POST_COUNT]
    context_object_name = 'posts'


@login_required
@require_POST
def like_post(request: WSGIRequest) -> JsonResponse:
    post_id = request.POST.get('post_id')

    action = dispatch_like_action(
        action=request.POST.get('action'),
        post=get_object_or_404(Post, id=post_id),
        my_user=request.user,
    )
    return JsonResponse({'action': action})


@login_required
@require_POST
def create_reply(request: WSGIRequest) -> JsonResponse:
    if (form := ReplyForm(request.POST)).is_valid():
        cd = form.cleaned_data
        post_id = request.POST.get('post_id')

        reply = Reply.objects.create(
            content=cd['content'],
            post=get_object_or_404(Post, id=post_id),
            user=request.user,
            parent=cd['parent'],
        )

        template_name = \
            'post/posts/post/replies/list/replyItem/item_generated.html'
        return render(request, template_name, {'reply': reply})
    else:
        lg.warning(f'Reply errors {form.errors}')
        return JsonResponse({'is_errors': True})


@login_required
@require_POST
def download_replies(request: WSGIRequest) -> HttpResponse:
    """Custom pagination logic"""

    page = int(request.POST.get('page'))
    post_id = request.POST.get('post_id')
    replies = Reply.objects.filter(post_id=post_id)

    start = page * settings.REQUEST_REPLY_COUNT + SHOWED_REPLY_COUNT
    end = (page + 1) * settings.REQUEST_REPLY_COUNT + SHOWED_REPLY_COUNT

    sliced_replies = replies[start:end]

    reply_stacks_over = end >= replies.count()

    if reply_stacks_over:

        remains = sliced_replies.exists()

        if remains:
            template_name = 'post/posts/post/replies/list/list_generated.html'
            template = render_to_string(
                request=request,
                template_name=template_name,
                context={'replies': sliced_replies},
            )

            new_context = {
                'replies': template,
                'completion': True,
            }
            return JsonResponse(new_context)
        else:
            context = {
                'completion': True,
                'no_data': True,
            }
            return JsonResponse(context)
    else:
        context = {
            'replies': sliced_replies,
        }
        template_name = 'post/posts/post/replies/list/list_generated.html'
        return render(request, template_name, context)


@login_required
@require_GET
def download_posts(request: WSGIRequest) -> HttpResponse:
    posts = Post.objects.all()

    if owner_id := request.GET.get('owner_user_id'):
        posts = posts.filter(user_id=owner_id)

    if query := request.GET.get('query'):
        searcher: BaseSearchQuerySet = PostsSearchQuerySet(
            queryset=Post.objects.all(),
            query=query,
        )
        posts = searcher.search()

    downloader = PageQuerySetDownloader(
        request=request,
        page=request.GET.get('page'),
        queryset=posts,
        per_page_count=settings.REQUEST_POST_COUNT,
        context_object_name='posts',
        template_name='post/posts/postsListGenerated/postsListGenerated.html',
        mixins=(AddReplyFormMixin, LikeActionListMixin),
    )
    return downloader.render()


@login_required
@require_POST
def create_post(request: WSGIRequest) -> JsonResponse:
    form = PostForm(data=request.POST, files=request.FILES)

    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()

        post.action = LikeAction.LIKE
        post.likes_count = 0
        post.reply_count = 0

        post_html = render_to_string(
            request=request,
            template_name='post/posts/post/post.html',
            context={'post': post, 'reply_form': ReplyForm()},
        )

        return JsonResponse({'post': post_html})
    else:
        return JsonResponse({
            'is_errors': True,
            'errors_list': form.errors,
        })


@login_required
@require_GET
def search_posts(request: WSGIRequest) -> HttpResponse:
    query = request.GET.get('query')
    searcher: BaseSearchQuerySet = PostsSearchQuerySet(
        queryset=Post.objects.all(),
        query=query,
    )
    posts = searcher.search()

    mixins_context = get_posts_mixins_context(
        posts=posts,
        request=request,
    )

    context = {
        **mixins_context,
        'query': query,
    }
    template_name = 'post/posts/postsListGenerated/postsListGenerated.html'
    return render(request, template_name, context)


@login_required
@require_GET
def filter_users(request: WSGIRequest) -> HttpResponse:
    posts = Post.objects.all()

    # FILTERS BY TAGS | ASC/DESC

    template_name = 'post/posts/postsListGenerated/postsListGenerated.html'
    context = {
        'posts': posts[:settings.REQUEST_POST_COUNT],
    }
    return render(request, template_name, context)


def get_posts_mixins_context(posts: QuerySet[Post],
                             request: WSGIRequest) -> dict:
    _request = request

    class Returns:
        def get_context_data(self, **kwargs):
            kwargs['posts'] = self.object_list[:settings.REQUEST_POST_COUNT]
            return kwargs

    class MixinsToFunc(
        AddReplyFormMixin,
        AddPostForm,
        LikeActionListMixin,
        Returns
    ):
        object_list = posts
        request = _request

    return MixinsToFunc().get_context_data()