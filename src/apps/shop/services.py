from django.db.models import F
from django.shortcuts import get_object_or_404
from django.urls import reverse

from apps.shop.models import Product, Cart, CartProduct
from main import settings


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


def get_payment_success_callback_url():
    path = reverse('payment-success')
    return f'{settings.PROTOCOL}://{settings.DOMAIN_NAME}{path}'


def create_order(user):
    from yookassa import Payment
    from yookassa.domain.models.currency import Currency
    from yookassa.domain.models.receipt import Receipt
    from yookassa.domain.common.confirmation_type import ConfirmationType
    from yookassa.domain.request.payment_request_builder import PaymentRequestBuilder
    from django.utils import timezone

    cart = get_user_cart(user)
    total_price = cart.get_total_price()
    cart.status = Cart.STATUS.PENDING
    cart.computed_sum = total_price
    cart.order_at = timezone.now()

    builder = PaymentRequestBuilder()
    builder.set_amount({"value": int(total_price), "currency": Currency.RUB})
    builder.set_confirmation({"type": ConfirmationType.REDIRECT, "return_url": get_payment_success_callback_url()})
    builder.set_capture(False)
    builder.set_description(f"Заказ {cart.id}")
    builder.set_metadata({"orderNumber": str(cart.id)})
    # builder.set_receipt(Receipt(...))
    request = builder.build()
    res = Payment.create(request)
    cart.payment_id = res.id
    cart.save()
    return res.id
