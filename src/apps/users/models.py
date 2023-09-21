from django.contrib.auth.models import AbstractUser
from apps.shop.models import Product
from django.db import models


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()