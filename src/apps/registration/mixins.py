import logging

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse

lg = logging.getLogger(__name__)


class UserSuccessUrlMixin:
    def get_success_url(self):
        return reverse('account:detail', args=(self.request.user.username,))


class ResetPasswordSuccessUrlMixin:
    def get_success_url(self):
        if isinstance(self.request.user, AnonymousUser):
            return reverse(settings.LOGIN_URL)
        else:
            return reverse(
                'account:detail', args=(self.request.user.username,)
            )
