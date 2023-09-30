from django.http import JsonResponse

from apps.account.pages.profile.forms import AccountEditForm


class AjaxErrorsMixin:
    @staticmethod
    def form_invalid(form: AccountEditForm) -> JsonResponse:
        form._errors['is_errors'] = True
        return JsonResponse(form._errors)
