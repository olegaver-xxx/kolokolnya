from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

# class ItemModel(models.Model):
#     name = models.CharField(max_length=200)
#     price = models.DecimalField(max_digits=5, decimal_places=2)
#     description = models.TextField()
#
#
# class Cart(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#
#
# class CartItem(models.Model):
#     product = models.ForeignKey(ItemModel, on_delete=models.CASCADE)
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
