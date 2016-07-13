# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-12 20:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_remove_userinventoryitem_no_stolen'),
    ]

    operations = [
        migrations.RenameField(
            model_name='background',
            old_name='icon',
            new_name='background',
        ),
        migrations.RemoveField(
            model_name='background',
            name='price_high',
        ),
        migrations.RemoveField(
            model_name='background',
            name='price_low',
        ),
        migrations.RemoveField(
            model_name='background',
            name='price_med',
        ),
        migrations.AddField(
            model_name='background',
            name='description',
            field=models.TextField(default='Пусто', verbose_name='Описание фона'),
        ),
        migrations.AddField(
            model_name='background',
            name='quality',
            field=models.IntegerField(choices=[(1, 'Стандартный фон'), (2, 'Редкий фон'), (3, 'Коллекционный фон')], default=1, verbose_name='Частота'),
        ),
    ]