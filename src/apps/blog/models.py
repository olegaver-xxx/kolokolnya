from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from ckeditor.fields import RichTextField


class ArticleModel(models.Model):
    article_title = models.CharField('Название статьи', max_length=40)
    # article_text = models.TextField('Текст статьи')
    content = RichTextField('Текст статьи')
    published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.article_title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class ImageModel(models.Model):
    article = models.ForeignKey(ArticleModel, related_name='images', on_delete=models.CASCADE)
    image = ThumbnailerImageField(upload_to='gallery/', blank=True, null=True)
    index = models.PositiveIntegerField(default=0, blank=True)











# class ArticleToImagModel(models.Model):
#     article = models.ForeignKey(ArticleModel, on_delete=models.CASCADE)
#     image = models.ForeignKey(ImageModel, on_delete=models.CASCADE)
#     index = models.PositiveIntegerField()

