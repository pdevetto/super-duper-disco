# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-11 13:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0018_auto_20161211_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='clean',
            field=models.IntegerField(default=0, null=True),
        ),
    ]