# Generated by Django 4.2.1 on 2023-06-19 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_product_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(blank=True, choices=[('Clothing', 'Clothing'), ('Home décor', 'Home décor'), ('Beauty & Personal Care', 'Beauty & Personal Care'), ('Fitness', 'Fitness'), ('Pet products', 'Pet products')], max_length=35),
        ),
    ]
