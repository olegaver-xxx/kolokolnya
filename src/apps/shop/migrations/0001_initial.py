# Generated by Django 4.2.5 on 2023-09-10 11:33

from django.db import migrations, models
import easy_thumbnails.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ItemModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
                ('description', models.TextField(max_length=400)),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(blank=True, null=True, upload_to='images/')),
            ],
        ),
    ]
