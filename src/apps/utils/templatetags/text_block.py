from django import template
from django.utils.safestring import mark_safe

from ..services import get_text_block_content

register = template.Library()


@register.simple_tag
def text_block(block_name, *args):
    text = get_text_block_content(block_name)
    if text is None:
        text = f'<span style="color:red;background-color: black;">[missing block "{block_name}"]</span>'
    return mark_safe(text)
