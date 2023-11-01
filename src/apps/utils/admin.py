import re

from django.contrib import admin
from django.utils.html import strip_tags
from django.utils.text import Truncator
from .models import TextBlockModel, SiteImages


@admin.register(TextBlockModel)
class TextBlockAdmin(admin.ModelAdmin):
    list_display = 'name', 'text_preview'

    def text_preview(self, obj):
        text = Truncator(re.sub(r"&\w+;", " ", strip_tags(obj.text))).words(10, truncate='...')
        return text


admin.site.register(SiteImages)