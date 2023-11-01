import os

from ckeditor.fields import RichTextField
from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from main.settings import DATA_DIR

class Preferences(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    prefs = models.JSONField(default=dict, blank=True)


class TextBlockModel(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    text = RichTextField(blank=True)
    name = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Блок текста'
        verbose_name_plural = 'Блоки текста'


class SiteImages(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)
    image = ThumbnailerImageField(upload_to='prefs/')

    def __str__(self):
        return self.name or os.path.basename(self.image.path)

    class Meta:
        verbose_name = 'Изоражение Сайта'
        verbose_name_plural = 'Изоражения Сайта'

