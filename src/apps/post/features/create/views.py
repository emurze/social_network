import logging

from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from apps.post.features.create.forms import PostForm

lg = logging.getLogger(__name__)


@login_required
@require_POST
def create_post(request: WSGIRequest) -> JsonResponse:
    lg.debug(request.POST)

    if (form := PostForm(request.POST)).is_valid():
        cd = form.cleaned_data

        lg.debug(f'Great action with {cd}')

        return JsonResponse({})
    else:
        return JsonResponse({
            'is_errors': True,
            'errors_list': form.errors
        })
