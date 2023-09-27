from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Product, Cart
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin



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
    model = Cart
    context_object_name = 'cart'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx['images'] = self.object_list.images_cart.all()
        return ctx