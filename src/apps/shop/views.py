import json

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage
from .forms import ProductForm, ImageForm
from .models import Product, Cart, CartProduct, ProductImage, Tag, Order
from django.views.generic import DetailView, ListView, TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from . import services as shop_services
from yookassa import Configuration


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

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data()
        ctx['cart_items'] = [x.product.id for x in shop_services.get_cart_products(self.request.user)]
        filtered_products, selected, tags = self.filter_products()
        ctx['selected'] = selected
        ctx['filtered'] = filtered_products
        ctx['tags'] = tags
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

    def post(self, product_id):
        product_id = self.request.POST.get('product_id')
        count = shop_services.add_product_to_cart(product_id, self.request.user)
        return JsonResponse({'status': 'ok', 'count': count})


class CartView(ListView):
    template_name = 'shop-cart.html'
    model = CartProduct
    context_object_name = 'products'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(cart__user=self.request.user.id, cart__status=Cart.STATUS.COLLECTING)
        return qs


class UpdateCartView(LoginRequiredMixin, View):

    def post(self, product_id):
        for key in self.request.POST:
            if key.startswith('quantity-'):
                item_id = int(key.split('-')[-1])
                count = self.request.POST[key]
                shop_services.update_product_to_cart(item_id, self.request.user, count)
        if 'pay' in self.request.POST:
            payment_url, order_id = shop_services.create_order(user=self.request.user)
            return HttpResponseRedirect(payment_url)
        else:
            return redirect(reverse('cart'))


class RemoveCartItemView(LoginRequiredMixin, View):
    def get(self, request, item_id):
        shop_services.delete_cart_item(item_id, request.user)
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


class SearchView(ListView):
    template_name = 'search-test.html'
    context_object_name = 'search'

    def get_queryset(self):
        qs = self.request.GET.get('q')
        results = Product.objects.filter(name__icontains=qs)
        return results

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data()
        ctx['cart_items'] = [x.product.id for x in shop_services.get_cart_products(self.request.user)]
        return ctx


# def search(request):
#     query = request.GET.get('q')
#     results = Product.objects.filter(name__icontains=query)
#     return render(request, 'search_results.html', {'products': results})


class ContactView(TemplateView):
    template_name = 'contact.html'


class OrderListView(ListView):
    model = Order
    template_name = 'orders_history.html'
    paginate_by = 10
    context_object_name = 'orders'


class OrderDetailView(DetailView):
    model = Product
    template_name = ...


@csrf_exempt
def payment_event(request):
    from yookassa.domain.notification import WebhookNotification
    event_json = json.loads(request.body)
    print(event_json)
    # {'type': 'notification', 'event': 'payment.waiting_for_capture',
    #  'object': {'id': '2cd081c3-000f-5000-8000-18fb1a9aa326', 'status': 'waiting_for_capture',
    #             'amount': {'value': '100.00', 'currency': 'RUB'}, 'description': 'Заказ 222',
    #             'recipient': {'account_id': '266415', 'gateway_id': '2131910'},
    #             'payment_method': {'type': 'bank_card', 'id': '2cd081c3-000f-5000-8000-18fb1a9aa326', 'saved': False,
    #                                'title': 'Bank card *4477',
    #                                'card': {'first6': '555555', 'last4': '4477', 'expiry_year': '2010',
    #                                         'expiry_month': '12', 'card_type': 'MasterCard', 'issuer_country': 'US'}},
    #             'created_at': '2023-10-29T14:36:51.955Z', 'expires_at': '2023-11-05T14:39:48.605Z', 'test': True,
    #             'paid': True, 'refundable': False, 'metadata': {'orderNumber': '222'},
    #             'authorization_details': {'rrn': '154342014456756', 'auth_code': '216410',
    #                                       'three_d_secure': {'applied': True, 'protocol': 'v1',
    #                                                          'method_completed': False, 'challenge_completed': True}}}}
    # try:
    #     notification_object = WebhookNotification(event_json)
    # except Exception:
    # # обработка ошибок
    #
    # # Получите объекта платежа
    # payment = notification_object.object
    return HttpResponse(status=200)
