from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from apps.account.mixins import ProfileSelectedMixin

User = get_user_model()


class AccountDetailView(LoginRequiredMixin, ProfileSelectedMixin, DetailView):
    model = User
    template_name = 'account/profile/profile.html'
    context_object_name = 'user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
