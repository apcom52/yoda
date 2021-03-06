# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-01 22:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0019_building_sprite'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbuild',
            name='game',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='game.Game', verbose_name='Игра'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userbuild',
            name='completed',
            field=models.BooleanField(default=False, verbose_name='Здание построено'),
        ),
        migrations.AlterField(
            model_name='userbuild',
            name='y',
            field=models.IntegerField(default=1, verbose_name='Координата Y'),
        ),
    ]
