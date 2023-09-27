import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.views.generic import CreateView
from rest_framework.generics import get_object_or_404

from apps.dashboard.services.create_action import create_action
from ..mixins import PostListViewMixin, LikeActionListMixin, \
    FilterPostsMixin, SearchPostsMixin, FilterOwnerMixin, \
    DefaultLimitPostsMixin, PostsMenuSelectedMixin
from apps.post.models import Post
from ..forms import PostForm, ReplyForm
from apps.post.services.like.action import LikeAction
from apps.post.services.like.dispatcher import dispatch_like_action
from django.conf import settings

lg = logging.getLogger(__name__)
SHOWED_REPLY_COUNT = 1


class PostListView(
    DefaultLimitPostsMixin,
    PostsMenuSelectedMixin,
    LikeActionListMixin,
    PostListViewMixin
):
    template_name = 'post/posts/posts.html'


class ResetPosts(
    LikeActionListMixin,
    DefaultLimitPostsMixin,
    PostListViewMixin
):
    template_name = 'post/posts/postsListGenerated/postsListGenerated.html'


def download_posts(request: WSGIRequest) -> HttpResponse:
    template_name = 'post/posts/postsListGenerated/postsListGenerated.html'
    paginate_by = settings.REQUEST_POST_COUNT
    queryset = Post.ext_objects.all()
    my_user = request.user

    queryset = FilterPostsMixin.filter(queryset, request.GET)

    if query := request.GET.get('query'):
        queryset = SearchPostsMixin.search(queryset, query)

    if owner_id := request.GET.get('owner_id'):
        queryset = FilterOwnerMixin.filter_by_owner(queryset, owner_id)

    queryset = Post.ext_objects.annotate_like_action(queryset, my_user)

    page = request.GET.get('page')
    paginator = Paginator(queryset, paginate_by)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        pass
    except EmptyPage:
        return HttpResponse('')

    context = {
        'page': int(page),
        'paginator': paginator,
        'posts': queryset,
        'reply_form': ReplyForm(),
    }
    return render(request, template_name, context)


class SearchPosts(
    LikeActionListMixin,
    DefaultLimitPostsMixin,
    SearchPostsMixin,
    PostListViewMixin,
):
    template_name = 'post/posts/postsListGenerated/postsListGenerated.html'


class FilterPosts(
    LikeActionListMixin,
    DefaultLimitPostsMixin,
    FilterPostsMixin,
    PostListViewMixin,
):
    template_name = 'post/posts/postsListGenerated/postsListGenerated.html'


class CreatePost(LoginRequiredMixin, CreateView):
    form_class = PostForm

    def form_valid(self, form: PostForm) -> JsonResponse:
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()

        create_action(self.request.user, 'creates post', post)

        post.action = LikeAction.LIKE
        post.likes_count = post.reply_count = 0

        post_html = render_to_string(
            request=self.request,
            template_name='post/posts/post/post.html',
            context={'post': post, 'reply_form': ReplyForm()},
        )
        return JsonResponse({'post': post_html})

    def form_invalid(self, form: PostForm) -> JsonResponse:
        lg.warning(f'Create post errors {form.errors}')
        return JsonResponse({'is_errors': True})


@login_required
@require_POST
def like_post(request: WSGIRequest) -> JsonResponse:
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)

    action = dispatch_like_action(
        action=request.POST.get('action'),
        post=post,
        my_user=request.user,
    )
    return JsonResponse({'action': action})
