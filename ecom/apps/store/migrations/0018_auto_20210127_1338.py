# Generated by Django 3.1.5 on 2021-01-27 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_auto_20210127_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='store',
            field=models.ForeignKey(blank=True, limit_choices_to={'groups__name': 'shop_owner'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='store.store'),
        ),
        migrations.AlterField(
            model_name='product',
            name='store',
            field=models.ForeignKey(blank=True, limit_choices_to={'groups__name': 'shop_owner'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.store'),
        ),
    ]
