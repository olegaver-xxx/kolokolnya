# Generated by Django 4.2.6 on 2023-11-12 13:01

from django.db import migrations, models
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0005_maingallery'),
    ]

    operations = [
        migrations.AddField(
            model_name='maingallery',
            name='description',
            field=models.CharField(default='IMAGE', max_length=35),
        ),
        migrations.AlterField(
            model_name='maingallery',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to='main-gallery/'),
        ),
    ]
