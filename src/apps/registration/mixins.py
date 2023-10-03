import logging

from django.urls import reverse

lg = logging.getLogger(__name__)


class UserSuccessUrlMixin:
    def get_success_url(self):
        return reverse('account:detail', args=(self.request.user.username,))
