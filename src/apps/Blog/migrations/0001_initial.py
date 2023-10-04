# Generated by Django 4.2.5 on 2023-10-04 07:25

from django.db import migrations, models
import django.db.models.deletion
import easy_thumbnails.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_title', models.CharField(max_length=40, verbose_name='Название статьи')),
                ('article_text', models.TextField(max_length=2000, verbose_name='Текст статьи')),
                ('published', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='gallery/')),
                ('index', models.PositiveIntegerField()),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='Blog.articlemodel')),
            ],
        ),
    ]
