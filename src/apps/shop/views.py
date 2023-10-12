from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage
from .forms import ProductForm, ImageForm
from .models import Product, Cart, CartProduct, ProductImage
from django.views.generic import DetailView, ListView, TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from . import services as shop_services


class ProductListView(ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'
    queryset = Product.objects.all().prefetch_related('images')
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data()
        ctx['cart_items'] = [x.product.id for x in shop_services.get_cart_products(self.request.user)]

        return ctx


class ProductDetailView(DetailView):
    template_name = 'product_detail.html'
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx['images'] = self.object.images.all()
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
        qs = qs.filter(cart__user=self.request.user.id)
        return qs







class UpdateCartView(LoginRequiredMixin, View):

    def post(self, product_id):
        for key in self.request.POST:
            if key.startswith('quantity-'):
                item_id = int(key.split('-')[-1])
                count = self.request.POST[key]
                shop_services.update_product_to_cart(item_id, self.request.user, count)
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
    template_name = 'search_results.html'
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



