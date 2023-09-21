from django.conf import settings
from django.forms import SelectDateWidget


class BirthdayDateWidget(SelectDateWidget):
    years = tuple(
        reversed(
            range(settings.CURRENT_YEAR - settings.OLDEST_HUMAN,
                  settings.CURRENT_YEAR)
        )
    )
    is_required = False

    def __init__(self, attrs=None, years=None, months=None, empty_label=None):
        super().__init__(
            attrs=attrs,
            years=years or self.years,
            months=months,
            empty_label=empty_label or ("Year", "Month", "Day")
        )

    def get_context(self, name, value, attrs):
        old_state = self.is_required
        self.is_required = False
        context = super().get_context(name, value, attrs)
        self.is_required = old_state
        return context
