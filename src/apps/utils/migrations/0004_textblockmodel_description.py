# Generated by Django 4.2.6 on 2023-11-03 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0003_siteimages_alter_textblockmodel_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='textblockmodel',
            name='description',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]