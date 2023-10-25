from django.contrib import admin
from .models import Product, ProductImage, Cart, CartProduct, Tag, Order


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class CartProductInline(admin.TabularInline):
    model = CartProduct


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartProductInline]
    fields = 'user', 'active'


admin.site.register(Tag)
admin.site.register(Order)

# @admin.register(CartProduct)
# class CartProductAdmin(admin.ModelAdmin):
#     list_display = 'cart', 'product', 'quantity'
#