from django import template

register = template.Library()


@register.filter(is_safe=False)
def minus(value: int, arg: int):
    """Add the arg to the value."""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return ""
