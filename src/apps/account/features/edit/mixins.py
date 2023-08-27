import json
import logging

from django.http import HttpResponse

from apps.account.features.edit.forms import AccountEditForm

lg = logging.getLogger(__name__)


class AjaxErrorsMixin:
    def form_invalid(self, form: AccountEditForm) -> HttpResponse:
        form._errors['is_errors'] = True
        return HttpResponse(json.dumps(form._errors))
