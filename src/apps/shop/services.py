from django.db.models import F
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
import math
from apps.shop.forms import RecordForm
from apps.shop.models import Product, Cart, CartProduct, Record, CartRecord
from main import settings
from apps.utils.yookassa import get_credentials
from yookassa import Configuration, Payment
from yookassa.domain.models.currency import Currency
from yookassa.domain.models.receipt import Receipt
from yookassa.domain.common.confirmation_type import ConfirmationType
from yookassa.domain.request.payment_request_builder import PaymentRequestBuilder
from django.utils import timezone
from tasks.payment_tasks import on_order_changed


def get_record_data():
    return dict(
        names_per_cost=5,
        cost=10,
        max_word_length=20
    )


def calculate_record_price(descriptions):
    rec_data = get_record_data()
    words_count = len(descriptions.strip().split())
    total_cost = math.ceil(words_count / rec_data['names_per_cost']) * rec_data['cost']
    return total_cost


def add_record_to_cart(record, user):
    price = calculate_record_price(record.description)
    record.cost = price
    cart = get_user_cart(user)
    record.cart = cart
    record.save()


def delete_record(rec_id, user):
    record = Record.objects.get(id=rec_id, cart__user=user)
    record.delete()


def get_record_for_cart(user):
    cart = get_user_cart(user)
    records = cart.records.all()
    return records


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
    if user.is_authenticated:
        return Cart.objects.filter(user=user, status=Cart.STATUS.COLLECTING).first() or create_user_cart(user)


def get_pending_cart(user) -> Cart:
    if user.is_authenticated:
        return Cart.objects.filter(user=user, status=Cart.STATUS.PENDING).first()


def create_user_cart(user):
    return Cart.objects.create(user=user)


def get_cart_item(product_id, user) -> CartProduct | None:
    cart = get_user_cart(user)
    if not cart:
        return None
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
    if not cart:
        return []
    return cart.cartproduct_set.all().prefetch_related('product')


def get_cart_item_ids(user):
    return CartProduct.objects.filter(cart__user=user).values_list('id', flat=True)


def get_payment_success_callback_url():
    path = reverse('payment-success')
    return f'{settings.PROTOCOL}://{settings.DOMAIN_NAME}{path}'


def create_order(user):
    if not user.is_authenticated:
        raise Http404

    shop_id, api_key = get_credentials()
    Configuration.account_id = str(shop_id)
    Configuration.secret_key = api_key

    cart = get_user_cart(user)
    total_price = cart.get_total_price()
    record = cart.records.last()
    if record:
        total_price += record.cost
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
    on_order_changed.send(cart.id)
    return res.confirmation.confirmation_url, res.id


def confirm_payment(user):
    cart = get_pending_cart(user)
    payment_id = cart.payment_id
    payment = Payment.find_one(payment_id)
    payment.capture()
    cart.status = Cart.STATUS.COMPLETED
    cart.save()
    on_order_changed.send(cart.id)
    redirect = get_payment_success_callback_url()
    return redirect

#
# def complete_order(user):
#     from yookassa.domain.request.payment_request_builder import PaymentRequestBuilder
#     from yookassa.domain.models.currency import Currency
#     from yookassa import Payment
#     import uuid
#     builder = PaymentRequestBuilder()
#     cart = get_pending_cart(user)
#     total_price = cart.get_total_price()
#     payment_id = cart.payment_id
#     idempotence_key = str(uuid.uuid4())
#     response = Payment.capture(
#         payment_id, builder.set_amount({"value": int(total_price), "currency": Currency.RUB}),
#         idempotence_key
#     )
#     return response


def update_order(order_id, status):
    order = get_object_or_404(Cart, id=order_id)
    order.status = status
    order.save()
    on_order_changed.send(order.id)
    return order


def order_changed_event(order_id: int):
    order = get_object_or_404(Cart, id=order_id)
    from .models import Cart as Order
    if order.status == Order.STATUS.CANCELED:
        # add log message
        pass
    elif order.status == Order.STATUS.COMPLETED:
        # send admin notification
        pass
    elif order.status == Order.STATUS.PENDING:
        pass
