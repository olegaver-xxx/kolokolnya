from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import JsonResponse
from .models import Product, Cart, CartProduct
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.decorators.csrf import csrf_exempt



class ProductListView(View):

    def get(self, request):
        products = Product.objects.all()
        return render(request, 'shop.html', {'products': products})


class ProductDetailView(DetailView):
    template_name = 'product_detail.html'
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx['images'] = self.object.images.all()
        return ctx
    # def get(self, request, product_id):
    #     product = get_object_or_404(Product, id=product_id)
    #     return render(request, 'product_detail.html', {'product': product})


class AddCartView(View, LoginRequiredMixin):

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user, product=product)
        cart.quantity += 1
        cart.save()
        return redirect('products:product_list')


class CartView(ListView):
    template_name = 'shop-cart.html'
    model = CartProduct
    context_object_name = 'products'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(cart__user=self.request.user.id)
        return qs

    # def get_context_data(self, **kwargs):
    #     ctx = super().get_context_data()
    #     ctx['products'] = self.object_list.all()
    #     return ctx


def add_to_cart(request):
    product_id = request.POST.get('product_id')
    print(f"Add product {product_id} to {request.user}", flush=True)
    return JsonResponse({'status': 'ok', 'count': 2})


@csrf_exempt
def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        item = Product.objects.get(product_id=product_id)
        item.quantity = quantity
        item.save()

        return JsonResponse({'result': 'ok'})
    else:
        return JsonResponse({'result': 'nok'})