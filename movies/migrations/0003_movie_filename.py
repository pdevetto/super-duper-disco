# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-28 15:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20161128_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='filename',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
