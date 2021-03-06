# Generated by Django 3.1.4 on 2021-01-27 22:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
        ('store', '0025_auto_20210127_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storeadmin',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='store', to='store.store'),
        ),
        migrations.AlterField(
            model_name='storeadmin',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to='userprofile.userprofile'),
        ),
    ]
