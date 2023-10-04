from django.contrib import messages as ms
from django.contrib.auth.views import PasswordResetConfirmView

from apps.registration.mixins import ResetPasswordSuccessUrlMixin


class MyPasswordResetConfirmView(
    ResetPasswordSuccessUrlMixin,
    PasswordResetConfirmView
):
    def form_valid(self, form):
        ms.success(self.request, 'Password successfully reset.')
        return super().form_valid(form)
