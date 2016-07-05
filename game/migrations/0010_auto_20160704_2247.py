# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-04 19:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0009_dogma'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tooltip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tooltip', models.CharField(max_length=256, verbose_name='Подсказка')),
            ],
            options={
                'verbose_name': 'Подсказка',
                'verbose_name_plural': 'Подсказки',
            },
        ),
        migrations.AlterModelOptions(
            name='dogma',
            options={'verbose_name': 'Догмат', 'verbose_name_plural': 'Догматы'},
        ),
    ]
