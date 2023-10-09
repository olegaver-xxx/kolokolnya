from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from apps.users.models import User
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    price = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.cart.user} / {self.product}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    # gallery_cart = models.ForeignKey(CartProduct, related_name='images_cart', on_delete=models.CASCADE)
    image = ThumbnailerImageField(upload_to='products/', blank=True, null=True)


