# Generated by Django 4.2.6 on 2023-12-05 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_alter_cartproduct_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='order_details',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
