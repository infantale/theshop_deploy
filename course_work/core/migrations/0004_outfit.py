# Generated by Django 3.2 on 2021-05-12 09:39

import core.utilities
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210508_1310'),
    ]

    operations = [
        migrations.CreateModel(
            name='Outfit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Описание')),
                ('price', models.FloatField(default=0, verbose_name='Цена')),
                ('image', models.ImageField(upload_to=core.utilities.get_timestamp_path, verbose_name='Изображение')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор образа')),
            ],
        ),
    ]
