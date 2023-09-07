from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField


class ItemModel(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField(max_length=400)
    image = ThumbnailerImageField(upload_to='images/', blank=True, null=True)
