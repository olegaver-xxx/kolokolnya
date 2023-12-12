import base64
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from .forms import ProductForm, ImageForm, RecordForm
from .models import Product, Cart, CartProduct, ProductImage, Tag, Order, Record
from django.views.generic import DetailView, ListView, TemplateView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from . import services as shop_services


class ProductListView(ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'
    queryset = Product.objects.all().prefetch_related('images')
    paginate_by = 10

    def filter_products(self):
        tags = Tag.objects.all()
        filtered_products = Product.objects.all()
        selected = self.request.GET.getlist('tag')
        if selected:
            filtered_products = filtered_products.filter(tags__tag=selected)
        return filtered_products, selected, tags

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(name__icontains=query)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx['cart_items'] = [x.product.id for x in shop_services.get_cart_products(self.request.user)]
        filtered_products, selected, tags = self.filter_products()
        ctx['selected'] = selected
        ctx['filtered'] = filtered_products
        ctx['tags'] = tags
        ctx['q'] = self.request.GET.get('q', '')
        return ctx


# class TagsFilteringView(ListView):
#     template_name = 'tags_search.html'
#     model = Product
#     context_object_name = 'tags_filter'
#
#     def get_queryset(self):
#         tags = Tag.objects.all()
#         selected = self.request.GET.getlist('tag')
#         results = Product.objects.filter(tags__tag__in=selected)
#         return results


class ProductDetailView(DetailView):
    template_name = 'product_detail.html'
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx['images'] = self.object.images.all()
        ctx['cart_items'] = [x.product.id for x in shop_services.get_cart_products(self.request.user)]
        return ctx


class AddCartView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        product_id = self.request.POST.get('product_id')
        count = shop_services.add_product_to_cart(product_id, self.request.user)
        return JsonResponse({'status': 'ok', 'count': count})


# class AddRecordView(LoginRequiredMixin, View):
#
#     def post(self, request, *args, **kwargs):
#         description = self.request.POST.get('description')
#         # total_price = shop_services.calculate_record_price(description)
#         try:
#             shop_services.add_record_to_cart(description, self.request.user)
#         except Exception as e:
#             pass
#         return HttpResponseRedirect(reverse('cart'))
#         # return JsonResponse({'status': 'ok', 'price': total_price}), rec_item


class CartView(LoginRequiredMixin, ListView):
    template_name = 'shop-cart.html'
    model = CartProduct
    context_object_name = 'products'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(cart__user=self.request.user.id, cart__status=Cart.STATUS.COLLECTING)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx['records'] = shop_services.get_record_for_cart(self.request.user)
        return ctx


class UpdateCartView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        for key in self.request.POST:
            if key.startswith('quantity-'):
                item_id = int(key.split('-')[-1])
                count = self.request.POST[key]
                shop_services.update_product_to_cart(item_id, self.request.user, count)
                return redirect(reverse('cart'))
            if key == 'delivery_info':
                data: str = self.request.POST[key]
                delivery_info = base64.decodebytes(data.encode('utf8')).decode('utf8')
                shop_services.update_delivery_info(json.loads(delivery_info), self.request.user)
        return redirect(reverse('cart'))


def make_order(request):
    payment_url, order_id = shop_services.create_order(user=request.user)
    return HttpResponseRedirect(payment_url)


class RemoveCartItemView(LoginRequiredMixin, View):
    def get(self, request, item_id, *args, **kwargs):
        shop_services.delete_cart_item(item_id, request.user)
        return redirect(reverse('cart'))


class RemoveRecord(LoginRequiredMixin, View):
    def get(self, request, rec_id, *args, **kwargs):
        shop_services.delete_record(rec_id, request.user)
        return redirect(reverse('cart'))


def create_gallery(request):
    if request.method == 'POST':
        gallery_form = ProductForm(request.POST)
        image_forms = [ImageForm(request.POST, request.FILES, prefix=str(x)) for x in range(4)] # создаем 3 формы для изображений
        if gallery_form.is_valid() and all([form.is_valid() for form in image_forms]):
            gallery = gallery_form.save() # сохраняем галерею
            for form in image_forms:
                image = form.save(commit=False) # сохраняем изображение без коммита (еще не привязано к галерее)
                image.gallery = gallery # привязываем изображение к созданной галерее
                image.save() # сохраняем изображение с привязкой к галерее
            return redirect('gallery_list') # перенаправляем на список галерей
    else:
        gallery_form = ProductForm()
        image_forms = [ImageForm(prefix=str(x)) for x in range(4)] # создаем 3 пустые формы для изображений
    context = {
        'gallery_form': gallery_form,
        'image_forms': image_forms,
    }
    return render(request, 'add_item.html', context)


# class SearchView(ListView):
#     template_name = 'search-test.html'
#     context_object_name = 'search'
#
#     def get_queryset(self):
#         qs = self.request.GET.get('q')
#         results = Product.objects.filter(name__icontains=qs)
#         return results
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         ctx = super().get_context_data()
#         ctx['cart_items'] = [x.product.id for x in shop_services.get_cart_products(self.request.user)]
#         return ctx


# def search(request):
#     query = request.GET.get('q')
#     results = Product.objects.filter(name__icontains=query)
#     return render(request, 'search_results.html', {'products': results})


class ContactView(TemplateView):
    template_name = 'contact.html'


class OrderListView(LoginRequiredMixin, ListView):
    model = Cart
    template_name = 'orders_history.html'
    paginate_by = 10
    context_object_name = 'orders'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user).exclude(status=Cart.STATUS.COLLECTING)
        return qs


class OrderDetailView(DetailView):
    model = Cart
    template_name = 'order_detail.html'
    context_object_name = 'order'


class OrderDetail(DetailView):
    template_name = 'order_detail.html'
    model = Cart
    context_object_name = 'order'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user.id).exclude(status=Cart.STATUS.COLLECTING)
        return qs


# class MakeOrder(TemplateView):
#     template_name = 'make_order.html'
#
#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data()
#         cart = shop_services.get_user_cart(self.request.user)
#         ctx['delivery_cost'] = cart.order_details.get('delivery_info', {}).get('cashOfDelivery', 0) // 100
#         ctx['cart_items'] = [x.product.id for x in shop_services.get_cart_products(self.request.user)]
#         ctx['records'] = shop_services.get_record_for_cart(self.request.user)
#         ctx['total_sum'] = shop_services.get_order_total_price(cart)
#         ctx['is_empty'] = not any([ctx['cart_items'], ctx['records']])
#         return ctx

class MakeOrder(ListView):
    template_name = 'make_order.html'
    model = CartProduct
    context_object_name = 'order_items'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(cart__user=self.request.user.id, cart__status=Cart.STATUS.COLLECTING)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        cart = shop_services.get_user_cart(self.request.user)
        ctx['delivery_cost'] = cart.order_details.get('delivery_info', {}).get('cashOfDelivery', 0) // 100
        ctx['cart_items'] = [x.product.id for x in shop_services.get_cart_products(self.request.user)]
        ctx['records'] = shop_services.get_record_for_cart(self.request.user)
        ctx['total_sum'] = shop_services.get_order_total_price(cart)
        ctx['is_empty'] = not any([ctx['cart_items'], ctx['records']])
        return ctx


class RecordsView(LoginRequiredMixin, FormView):
    template_name = 'records.html'
    form_class = RecordForm
    success_url = reverse_lazy('cart')

    def get_initial(self):
        cart = shop_services.get_user_cart(self.request.user)
        data = {'cart': cart}
        return data

    def form_valid(self, form):
        rec = form.save()
        shop_services.add_record_to_cart(rec, self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        cart = shop_services.get_user_cart(self.request.user)
        rec = cart.records.last()
        if rec:
            kwargs['instance'] = rec
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx['record_info'] = shop_services.get_record_data()
        return ctx


@csrf_exempt
def payment_event(request):
    if not request.method == 'POST':
        return HttpResponseBadRequest('Bad request')
    from yookassa.domain.notification import WebhookNotification
    event_json = json.loads(request.body)
    # {'type': 'notification',
    #  'event': 'payment.waiting_for_capture',
    #  'object': {
    #       'id': '2cd081c3-000f-5000-8000-18fb1a9aa326',
    #       'status': 'waiting_for_capture',
    #       'amount': {
    #           'value': '100.00',
    #           'currency': 'RUB'
    #       },
    #  'description': 'Заказ 222',
    #  'recipient': {'account_id': '266415', 'gateway_id': '2131910'},
    #  'payment_method': {
    #       'type': 'bank_card',
    #       'id': '2cd081c3-000f-5000-8000-18fb1a9aa326',
    #       'saved': False,
    #       'title': 'Bank card *4477',
    #       'card': {'first6': '555555', 'last4': '4477', 'expiry_year': '2010', 'expiry_month': '12', 'card_type': 'MasterCard', 'issuer_country': 'US'}
    #       },
    #  'created_at': '2023-10-29T14:36:51.955Z',
    #  'expires_at': '2023-11-05T14:39:48.605Z',
    #  'test': True,
    #  'paid': True,
    #  'refundable': False,
    #  'metadata': {'orderNumber': '222'},
    #  'authorization_details': {
    #      'rrn': '154342014456756',
    #      'auth_code': '216410',
    #      'three_d_secure': {'applied': True, 'protocol': 'v1', 'method_completed': False, 'challenge_completed': True}
    #      }
    #  }
    #  }
    try:
        notification_object = WebhookNotification(event_json)
    except Exception as e:
        # обработка ошибок
        raise Exception(f'Invalid notification object {e}, {event_json}')
    # Получите объекта платежа
    payment = notification_object.object
    order_id = int(payment.metadata['orderNumber'])
    shop_services.payment_success(order_id)
    return HttpResponse(status=200)


class PayedOrdersView(ListView):
    template_name = 'payed_carts.html'
    model = Cart
    context_object_name = 'payed_orders'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(status=Cart.STATUS.PAYED)


class CompletedOrdersView(ListView):
    template_name = 'completed_carts.html'
    model = Cart
    context_object_name = 'completed_orders'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(status=Cart.STATUS.COMPLETED)


class CompleteOrder(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        order_id = self.request.POST.get('order_id')
        complete = shop_services.compete_order(order_id)
        return JsonResponse({'order_id': order_id, 'complete': complete})
