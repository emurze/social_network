import logging
from typing import Any

lg = logging.getLogger(__name__)


class ProfileSelectedMixin:
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        user = self.object
        if self.request.user == user:
            kwargs['icon_menu__selected'] = 'profile'
            kwargs['is_owner'] = True
        return super().get_context_data(**kwargs)
