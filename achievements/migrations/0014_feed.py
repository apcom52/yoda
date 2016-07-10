# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-23 16:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('achievements', '0013_auto_20160622_2102'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='Дата публикации')),
                ('type', models.IntegerField(choices=[(0, 'Запись'), (1, 'Достижение'), (2, 'Случайный бонус'), (3, 'Продажа'), (4, 'Мероприятие'), (5, 'Опрос'), (6, 'Расписание'), (7, 'Заметки')], default=0, verbose_name='Тип записи')),
                ('value', models.TextField(verbose_name='Значение')),
                ('extra', models.TextField(blank=True, null=True, verbose_name='Дополнительные записи')),
                ('login', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]