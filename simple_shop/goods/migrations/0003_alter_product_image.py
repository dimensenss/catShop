# Generated by Django 4.2.16 on 2024-11-20 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_product_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product_images/%Y/%m/%d/'),
        ),
    ]
