from ckeditor.fields import RichTextField
from django.db import models


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
