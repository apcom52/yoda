# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-09 13:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_auto_20160717_0118'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='dust',
            field=models.IntegerField(default=0, verbose_name='Пыль'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='gold',
            field=models.IntegerField(default=0, verbose_name='Золото'),
        ),
    ]
