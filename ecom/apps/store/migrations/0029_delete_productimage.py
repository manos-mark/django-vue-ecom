# Generated by Django 3.1.5 on 2021-01-28 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0028_remove_product_parent'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProductImage',
        ),
    ]
