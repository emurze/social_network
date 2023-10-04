import logging

from django.contrib.auth.views import PasswordResetView

from apps.registration.mixins import ResetPasswordSuccessUrlMixin

lg = logging.getLogger(__name__)


class MyPasswordResetView(
    ResetPasswordSuccessUrlMixin,
    PasswordResetView
):
    pass
