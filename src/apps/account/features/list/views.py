import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import QuerySet
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import ListView

from apps.account.services.follow.dispatcher import dispatch_follow_action
from apps.account.services.follow.mixins import FollowActionListMixin

User = get_user_model()
lg = logging.getLogger(__name__)
DEFAULT_USER_COUNT = 15


@login_required
@require_POST
def follow_list(request: WSGIRequest) -> JsonResponse:
    username = request.POST.get('username')

    action = dispatch_follow_action(
        action=request.POST.get('action'),
        my_user=request.user,
        other_user=get_object_or_404(User, username=username)
    )
    return JsonResponse({'action': action})


class AccountListView(LoginRequiredMixin, FollowActionListMixin, ListView):
    template_name = 'account/users/users.html'
    context_object_name = 'users'

    def get_queryset(self) -> QuerySet[User]:
        return (User.objects
                    .order_by('username')
                    .exclude(id=self.request.user.id)[:DEFAULT_USER_COUNT])


@login_required
@require_GET
def download_users(request: WSGIRequest) -> HttpResponse:
    _request = request

    users = User.objects.all()
    paginator = Paginator(users, settings.REQUEST_USER_COUNT)

    page = request.GET.get('page')

    try:
        users = paginator.page(page)
    except (EmptyPage, PageNotAnInteger):
        return HttpResponse('')

    class Returns:
        def get_context_data(self, **kwargs):
            if not kwargs.get('users'):
                kwargs['users'] = self.object_list
            return kwargs

    class ClassToFunc(
        FollowActionListMixin,
        Returns,
    ):
        object_list = users
        request = _request

    context = ClassToFunc().get_context_data()

    template_name = 'account/users/userListGenerated/userListGenerated.html'
    return render(request, template_name, context)
