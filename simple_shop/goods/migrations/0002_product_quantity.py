# Generated by Django 4.2.16 on 2024-10-30 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='Кількість товару'),
        ),
    ]
