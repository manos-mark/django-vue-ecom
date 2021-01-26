# Generated by Django 3.1.4 on 2021-01-26 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_category_is_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='last_visit',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='num_visits',
            field=models.IntegerField(default=0),
        ),
    ]
