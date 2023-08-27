import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView

from apps.account.features.edit.forms import AccountEditForm
from apps.account.features.edit.mixins import AjaxErrorsMixin

lg = logging.getLogger(__name__)
User = get_user_model()


class AccountEditView(LoginRequiredMixin, AjaxErrorsMixin, UpdateView):
    model = User
    form_class = AccountEditForm
    template_name = 'account/edit/edit.html'
    context_object_name = 'user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        kwargs |= {'user': self.object}
        return super().get_context_data(**kwargs)
