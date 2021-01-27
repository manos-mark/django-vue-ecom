# Generated by Django 3.1.4 on 2021-01-27 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
        ('store', '0024_auto_20210127_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
        migrations.CreateModel(
            name='StoreAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='store', to='store.store')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='userprofile', to='userprofile.userprofile')),
            ],
        ),
    ]
