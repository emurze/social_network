import logging

from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Count
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from apps.post.features.create.forms import PostForm
from apps.post.features.list.forms import ReplyForm
from apps.post.services.like.action import LikeAction

lg = logging.getLogger(__name__)


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
            'errors_list': form.errors
        })
