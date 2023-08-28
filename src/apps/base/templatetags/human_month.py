from django import template

register = template.Library()

HUMAN_MONTHS = (
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)


@register.filter
def human_month(month: int) -> str:
    """Humanize int month."""
    try:
        index = int(month) - 1
        return HUMAN_MONTHS[index]
    except (ValueError, TypeError, IndexError, KeyError):
        return ""
