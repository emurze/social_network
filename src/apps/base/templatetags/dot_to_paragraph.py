from django import template
from django.utils.safestring import SafeString

register = template.Library()


@register.filter
def dot_to_paragraph(text: str) -> SafeString:
    if text[-1] == '.':
        text = text.rstrip('.')

    text_list = text.split('.')
    text_html = ''.join(f'<p>{string}</p>' for string in text_list)
    return SafeString(text_html)
