from django.db import models


class ShopModel(models.Model):
    title = models.CharField(max_length=25)
    description = models.TextField(max_length=200)
    # image = models.ImageField(upload_to=image/)
