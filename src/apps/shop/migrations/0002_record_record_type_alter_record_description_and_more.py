# Generated by Django 4.2.7 on 2023-12-14 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='record_type',
            field=models.IntegerField(choices=[(1, 'Панихида'), (2, 'Молебен'), (3, 'Сорокоуст'), (4, 'Заказная'), (5, 'Вечное поминовение'), (6, 'Именной кирпичик')], default=1, verbose_name='Записка'),
        ),
        migrations.AlterField(
            model_name='record',
            name='description',
            field=models.TextField(blank=True, max_length=10000, null=True, verbose_name='Список имён'),
        ),
        migrations.AlterField(
            model_name='record',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Ваша цена'),
        ),
    ]
