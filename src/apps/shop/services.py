from django.shortcuts import get_object_or_404
from apps.shop.models import Product, Cart, CartProduct


def add_product_to_cart(product_id, user, count=1):
    cart_item = get_cart_item(product_id, user)
    cart_item.quantity += count
    cart_item.save()
    return cart_item.quantity


def update_product_to_cart(item_id: int, user, count: int):
    cart_item = CartProduct.objects.get(id=item_id, cart__user=user)
    cart_item.quantity = count
    cart_item.save()
    return cart_item.quantity


def get_user_cart(user) -> Cart:
    return Cart.objects.get_or_create(user=user)[0]


def get_cart_item(product_id, user) -> CartProduct:
    cart = get_user_cart(user)
    product = get_object_or_404(Product, pk=product_id)
    cart_item, _ = CartProduct.objects.get_or_create(cart=cart, product=product)
    return cart_item


def remove_product_from_cart(product_id, user, count=1):
    cart_item = get_cart_item(product_id, user)
    cart_item.quantity -= count
    if cart_item.quantity <= 0:
        cart_item.delete()
        return 0
    else:
        cart_item.save()
        return cart_item.quantity


def delete_cart_item(item_id, user):
    cart_item = CartProduct.objects.get(id=item_id, cart__user=user)
    cart_item.delete()


def get_cart_products(user):
    cart = get_user_cart(user)
    return cart.cartproduct_set.all().prefetch_related('product')


def get_cart_item_ids(user):
    return CartProduct.objects.filter(cart__user=user).values_list('id', flat=True)

