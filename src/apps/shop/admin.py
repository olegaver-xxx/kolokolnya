from django.contrib import admin
from .models import Product, ProductImage, Cart, CartProduct, Tag, Order, Record
from django.db import models
from django_json_widget.widgets import JSONEditorWidget


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
    fields = 'user', 'active', 'status', 'computed_sum', 'payment_id', 'order_details'
    list_display = 'user', 'status', 'computed_sum', 'pk'
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }

admin.site.register(Tag)
# admin.site.register(Order)
admin.site.register(Record)

# @admin.register(CartProduct)
# class CartProductAdmin(admin.ModelAdmin):
#     list_display = 'cart', 'product', 'quantity'
#