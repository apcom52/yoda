# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-22 20:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0012_auto_20160416_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetable',
            name='earlier',
            field=models.BooleanField(default=False, verbose_name='Начнется раньше'),
        ),
    ]