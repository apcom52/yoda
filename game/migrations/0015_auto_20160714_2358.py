# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-14 20:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0014_game_step'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='culture',
            field=models.FloatField(default=0, verbose_name='Очки культуры'),
        ),
        migrations.AddField(
            model_name='game',
            name='faith',
            field=models.FloatField(default=0, verbose_name='Очки веры'),
        ),
        migrations.AddField(
            model_name='game',
            name='food',
            field=models.FloatField(default=0, verbose_name='Очки еды'),
        ),
        migrations.AddField(
            model_name='game',
            name='gold',
            field=models.FloatField(default=0, verbose_name='Очки золота'),
        ),
        migrations.AddField(
            model_name='game',
            name='happiness',
            field=models.FloatField(default=0, verbose_name='Очки настроения'),
        ),
        migrations.AddField(
            model_name='game',
            name='production',
            field=models.FloatField(default=0, verbose_name='Очки производства'),
        ),
        migrations.AddField(
            model_name='game',
            name='science',
            field=models.FloatField(default=0, verbose_name='Очки науки'),
        ),
        migrations.AddField(
            model_name='game',
            name='tourism',
            field=models.FloatField(default=0, verbose_name='Очки туризма'),
        ),
        migrations.AddField(
            model_name='step',
            name='culture',
            field=models.FloatField(default=0, verbose_name='Очки культуры за ход'),
        ),
        migrations.AddField(
            model_name='step',
            name='faith',
            field=models.FloatField(default=0, verbose_name='Очки веры за ход'),
        ),
        migrations.AddField(
            model_name='step',
            name='food',
            field=models.FloatField(default=0, verbose_name='Очки еды за ход'),
        ),
        migrations.AddField(
            model_name='step',
            name='gold',
            field=models.FloatField(default=0, verbose_name='Очки золота за ход'),
        ),
        migrations.AddField(
            model_name='step',
            name='happiness',
            field=models.FloatField(default=0, verbose_name='Очки настроения за ход'),
        ),
        migrations.AddField(
            model_name='step',
            name='production',
            field=models.FloatField(default=0, verbose_name='Очки производства за ход'),
        ),
        migrations.AddField(
            model_name='step',
            name='science',
            field=models.FloatField(default=0, verbose_name='Очки науки за ход'),
        ),
        migrations.AddField(
            model_name='step',
            name='tourism',
            field=models.FloatField(default=0, verbose_name='Очки туризма за ход'),
        ),
        migrations.AddField(
            model_name='userteach',
            name='game',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='game.Game', verbose_name='Игра'),
            preserve_default=False,
        ),
    ]
