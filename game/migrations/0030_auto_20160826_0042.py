# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-25 21:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0029_remove_technology_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='wonder',
            field=models.BooleanField(default=True, verbose_name='Чудо света'),
        ),
    ]
