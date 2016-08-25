# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-25 21:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0030_auto_20160826_0042'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='cost',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Содержание'),
        ),
        migrations.AlterField(
            model_name='building',
            name='wonder',
            field=models.BooleanField(default=False, verbose_name='Чудо света'),
        ),
    ]
