# Generated by Django 4.2.1 on 2023-06-02 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_product_is_open_product_winner_alter_product_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-updated']},
        ),
    ]
