# Generated by Django 3.1.4 on 2021-01-28 01:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0027_auto_20210127_2351'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='parent',
        ),
    ]
