# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-25 21:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0027_auto_20160825_0138'),
    ]

    operations = [
        migrations.AddField(
            model_name='technology',
            name='price',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Цена обслуживания'),
        ),
    ]
