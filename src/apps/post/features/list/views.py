import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import ListView
from rest_framework.generics import get_object_or_404

from apps.post.features.list.forms import ReplyForm
from apps.post.features.list.mixins import \
    AddPostQuerysetMixin, AddReplyFormMixin, PageLimitQuerysetMixin, \
    AddPostForm
from apps.post.models import Post, Reply
from apps.post.services.like.dispatcher import dispatch_like_action
from apps.post.services.like.mixins import LikeActionListMixin
from django.conf import settings

lg = logging.getLogger(__name__)
SHOWED_REPLY_COUNT = 1


class PostListView(
    LoginRequiredMixin,
    AddReplyFormMixin,

    AddPostForm,

    PageLimitQuerysetMixin,
    AddPostQuerysetMixin,

    LikeActionListMixin,
    ListView,
):
    template_name = 'post/posts/posts.html'
    context_object_name = 'posts'


@require_POST
def execute_like_action(request: WSGIRequest) -> JsonResponse:
    post_id = request.POST.get('post_id')

    action = dispatch_like_action(
        action=request.POST.get('action'),
        post=get_object_or_404(Post, id=post_id),
        my_user=request.user,
    )

    return JsonResponse({'action': action})


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


@require_POST
def download_replies_by_slice(request: WSGIRequest) -> HttpResponse:
    _slice = int(request.POST.get('slice'))
    post_id = request.POST.get('post_id')

    replies = Reply.objects.filter(post_id=post_id)

    start = _slice * settings.REQUEST_REPLY_COUNT + SHOWED_REPLY_COUNT
    end = (_slice + 1) * settings.REQUEST_REPLY_COUNT + SHOWED_REPLY_COUNT

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
    _request = request

    posts = AddPostQuerysetMixin().get_queryset()

    if user_id := request.GET.get('user_id'):
        posts = posts.filter(user_id=user_id)

    paginator = Paginator(posts, settings.REQUEST_POST_COUNT)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except (EmptyPage, PageNotAnInteger):
        return HttpResponse('')

    class Returns:
        def get_context_data(self, **kwargs):
            if not kwargs.get('posts'):
                kwargs['posts'] = self.object_list
            return kwargs

    class ClassToFunc(
        AddReplyFormMixin,
        LikeActionListMixin,
        Returns,
    ):
        object_list = posts
        request = _request

    context = ClassToFunc().get_context_data()

    template_name = 'post/posts/postsListGenerated/postsListGenerated.html'
    return render(request, template_name, context)
