from django.contrib import admin
from apps.shop.models import ItemModel
from apps.Blog.models import ArticleModel


admin.site.register(ItemModel)
admin.site.register(ArticleModel)
# Register your models here.
