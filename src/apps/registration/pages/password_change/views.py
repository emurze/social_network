from django.contrib import messages as ms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView

from apps.registration.mixins import UserSuccessUrlMixin


class MyPasswordChangeView(
    LoginRequiredMixin,
    UserSuccessUrlMixin,
    PasswordChangeView
):
    def form_valid(self, *args, **kwargs):
        ms.success(self.request, 'Password was successfully changed.')
        return super().form_valid(*args, **kwargs)
