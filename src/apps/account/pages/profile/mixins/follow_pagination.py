from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import TemplateView

User = get_user_model()


class AddFollowingUsersPaginationMixin(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        followings = self.get_queryset()
        page = int(self.request.GET.get('page'))

        if followings_exists := followings.exists():
            paginator = Paginator(
                followings,
                settings.REQUEST_FOLLOWINGS_COUNT
            )

            try:
                following_users = paginator.page(page)
            except PageNotAnInteger:
                following_users = paginator.page(1)
                page = 1
            except EmptyPage:
                following_users = paginator.page(paginator.num_pages)
                page = paginator.num_pages

            kwargs['following_users'] = following_users

        kwargs['page'] = page
        kwargs['exists_followings_users'] = followings_exists
        return super().get_context_data(**kwargs)
