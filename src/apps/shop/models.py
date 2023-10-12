from django.db import models
from django.db.models import F, Sum
from easy_thumbnails.fields import ThumbnailerImageField
from apps.users.models import User
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Cart(models.Model):
    class STATUS:
        COLLECTING = 'collecting'
        PENDING = 'pending'
        COMPLETED = 'completed'
        CANCELED = 'canceled'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order_at = models.DateTimeField(blank=True, null=True)
    payment_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=255, default=STATUS.COLLECTING, choices=(
        (STATUS.COLLECTING, 'Collecting'),
        (STATUS.PENDING, 'Pending Payment'),
        (STATUS.CANCELED, 'Canceled'),
        (STATUS.COMPLETED, 'Completed')
    ))
    computed_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_id = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def get_total_price(self):
        return CartProduct.objects.filter(cart=self).annotate(
            total=F('quantity') * F('product__price')
        ).aggregate(
            total_price=Sum('total')
        )['total_price']


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.cart.user} / {self.product}"

    def total_price(self):
        return self.product.price * self.quantity


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    # gallery_cart = models.ForeignKey(CartProduct, related_name='images_cart', on_delete=models.CASCADE)
    image = ThumbnailerImageField(upload_to='products/', blank=True, null=True)


# class Order(models.Model):
#     class STATUS:
#         PENDING = 'pending'
#         COMPLETED = 'completed'
#         CANCELED = 'canceled'
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=255, default=STATUS.PENDING, choices=(
#         (STATUS.PENDING, 'Pending'),
#         (STATUS.CANCELED, 'Canceled'),
#         (STATUS.COMPLETED, 'Completed')
#     ))
#     sum = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     bank_id = models.CharField(max_length=128, blank=True, null=True)
