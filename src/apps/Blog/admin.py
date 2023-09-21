from django.contrib import admin
from .models import ArticleModel, ImageModel, ArticleToImagModel


class ArticleImageInline(admin.TabularInline):
    model = ArticleToImagModel
    extra = 1


class ArticleModelAdmin(admin.ModelAdmin):
    inlines = [ArticleImageInline]


admin.site.register(ArticleModel, ArticleModelAdmin)
# admin.site.register(ImageModel)
