from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField


class ArticleModel(models.Model):
    article_title = models.CharField('Название статьи', max_length=40)
    article_text = models.TextField('Текст статьи', max_length=2000)
    published = models.DateTimeField()
    article_image = ThumbnailerImageField(upload_to='media/', blank=True, null=True)


class Image(models.Model):
    gallery = models.ManyToManyField(ArticleModel, through='GalleryImage')


class GalleryImage(models.Model):
    gallery = models.ForeignKey(ArticleModel, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    index = models.PositiveIntegerField()

