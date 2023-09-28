from django.contrib import admin
from .models import Product, ProductImage, Cart, CartProduct


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    fields = 'user', 'active'


admin.site.register(CartProduct)
