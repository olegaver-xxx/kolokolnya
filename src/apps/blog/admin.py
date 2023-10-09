from django.contrib import admin

from .forms import ArticleForm
from .models import ArticleModel, ImageModel


class ArticleImageInline(admin.TabularInline):
    model = ImageModel
    extra = 1


class ArticleModelAdmin(admin.ModelAdmin):
    inlines = [ArticleImageInline]


admin.site.register(ArticleModel, ArticleModelAdmin)

