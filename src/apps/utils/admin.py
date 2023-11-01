import re

from django.contrib import admin
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.utils.text import Truncator
from .models import TextBlockModel, SiteImages


@admin.register(TextBlockModel)
class TextBlockAdmin(admin.ModelAdmin):
    list_display = 'name', 'text_preview'

    def text_preview(self, obj):
        text = Truncator(re.sub(r"&\w+;", " ", strip_tags(obj.text))).words(10, truncate='...')
        return text


@admin.register(SiteImages)
class SiteImagesAdmin(admin.ModelAdmin):
    readonly_fields = 'url', 'preview'
    list_display = 'name', 'url'

    fields = 'name', 'image', 'url', 'preview'

    def url(self, obj):
        return obj.image.url

    def preview(self, obj):
        return mark_safe(f"<img src='{obj.image.url}' width='500px'>")
