from django import template
from django.utils.safestring import mark_safe

from ..services import get_text_block_content

register = template.Library()


@register.simple_tag
def text_block(block_name, *args):
    return mark_safe(get_text_block_content(block_name))
