# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-01 15:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_building_buildingbonus_buildingbonusmodificator_technology'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buildingbonus',
            name='building',
        ),
        migrations.RemoveField(
            model_name='buildingbonusmodificator',
            name='building',
        ),
        migrations.AddField(
            model_name='building',
            name='bonus',
            field=models.ManyToManyField(blank=True, to='game.BuildingBonus'),
        ),
    ]
