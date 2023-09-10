from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField


class ArticleModel(models.Model):
    article_title = models.CharField('Название статьи', max_length=40)
    article_text = models.TextField('Текст статьи', max_length=2000)
    article_image = ThumbnailerImageField(upload_to='media/', blank=True, null=True)
    published = models.DateTimeField()

