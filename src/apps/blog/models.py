from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField


class ArticleModel(models.Model):
    article_title = models.CharField('Название статьи', max_length=40)
    article_text = models.TextField('Текст статьи', max_length=2000)
    published = models.DateTimeField()

    def __str__(self):
        return self.article_title


class ImageModel(models.Model):
    article = models.ForeignKey(ArticleModel, related_name='images', on_delete=models.CASCADE)
    image = ThumbnailerImageField(upload_to='gallery/', blank=True, null=True)
    index = models.PositiveIntegerField()











# class ArticleToImagModel(models.Model):
#     article = models.ForeignKey(ArticleModel, on_delete=models.CASCADE)
#     image = models.ForeignKey(ImageModel, on_delete=models.CASCADE)
#     index = models.PositiveIntegerField()
