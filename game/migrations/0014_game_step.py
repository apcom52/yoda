# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-11 21:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0013_technology_branch'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_completed', models.BooleanField(default=False, verbose_name='Игра завершилась')),
                ('nation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Nation', verbose_name='Нация')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name_plural': 'Игры',
                'verbose_name': 'Игра',
            },
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step', models.IntegerField(verbose_name='Номер хода')),
                ('date', models.DateTimeField(verbose_name='Дата и время хода')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Game', verbose_name='Номер игры')),
            ],
            options={
                'verbose_name_plural': 'Ходы',
                'verbose_name': 'Ход',
            },
        ),
    ]
