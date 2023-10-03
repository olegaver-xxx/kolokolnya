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


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    products = models.ManyToManyField(Product, through='CartProduct')


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class ProductImage(models.Model):
    gallery = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    # gallery_cart = models.ForeignKey(CartProduct, related_name='images_cart', on_delete=models.CASCADE)
    image = ThumbnailerImageField(upload_to='products/', blank=True, null=True)