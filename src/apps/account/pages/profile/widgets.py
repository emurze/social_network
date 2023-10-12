import logging

from django.forms import ClearableFileInput

lg = logging.getLogger(__name__)


class MyPhoto(ClearableFileInput):
    current_user = None
    template_name = \
        "account/profile/edit_window/form/photoWidget/photoWidget.html"

    def get_context(self, name, value, attrs) -> dict:
        context = super().get_context(name, value, attrs)
        context['current_user'] = self.current_user
        return context | super().get_context(name, value, attrs)
