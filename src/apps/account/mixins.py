from typing import Any


class ProfileSelectedMixin:
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        kwargs |= {'icon_menu__selected': 'profile'}
        return super().get_context_data(**kwargs)
