from django.contrib import messages as ms
from django.contrib.auth.views import PasswordResetConfirmView

from apps.registration.mixins import UserSuccessUrlMixin


class MyPasswordResetConfirmView(
    UserSuccessUrlMixin,
    PasswordResetConfirmView,
):
    def form_valid(self, form):
        ms.success(self.request, 'Reset has been successfully performed.')
        return super().form_valid(form)
