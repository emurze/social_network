import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.views.generic import CreateView
from rest_framework.generics import get_object_or_404

from apps.dashboard.services.create_action import create_action
from apps.post.models import Reply, Post
from apps.post.pages.posts.forms import ReplyForm

lg = logging.getLogger(__name__)


class CreteReply(LoginRequiredMixin, CreateView):
    form_class = ReplyForm

    def form_valid(self, form: ReplyForm) -> HttpResponse:
        cd = form.cleaned_data
        post_id = self.request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)

        create_action(self.request.user, 'replies post', post)

        reply = Reply.objects.create(
            content=cd['content'],
            post=post,
            user=self.request.user,
            parent=cd['parent'],
        )

        return render(
            self.request,
            'post/posts/post/replies/list/replyItem/item_generated.html',
            {'reply': reply}
        )

    def form_invalid(self, form: ReplyForm) -> HttpResponse:
        lg.warning(f'Reply errors {form.errors}')
        return JsonResponse({'is_errors': True})


@login_required
@require_POST
def download_replies(request: WSGIRequest) -> HttpResponse:
    """Custom pagination logic"""

    template_name = 'post/posts/post/replies/list/list_generated.html'

    page = int(request.POST.get('page'))
    post_id = request.POST.get('post_id')
    replies = Reply.objects.filter(post_id=post_id)

    showed_reply_count = 1
    start = page * settings.REQUEST_REPLY_COUNT + showed_reply_count
    end = (page + 1) * settings.REQUEST_REPLY_COUNT + showed_reply_count

    sliced_replies = replies[start:end]
    reply_stacks_over = end >= replies.count()

    if reply_stacks_over:

        remains = sliced_replies.exists()

        if remains:
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
        return render(request, template_name, context)
