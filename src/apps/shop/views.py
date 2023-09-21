from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Product
from apps.users.models import Cart


class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'products/product_list.html', {'products': products})


class ProductDetailView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        return render(request, 'products/product_detail.html', {'product': product})


class CartView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user, product=product)
        cart.quantity += 1
        cart.save()
        return redirect('products:product_list')