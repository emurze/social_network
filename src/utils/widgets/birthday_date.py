import datetime

from django.forms import SelectDateWidget

NOW = datetime.date.today().year
OLDER_HUMAN = 122


class BirthdayDateWidget(SelectDateWidget):
    years = tuple(reversed(range(NOW - OLDER_HUMAN, NOW)))
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
