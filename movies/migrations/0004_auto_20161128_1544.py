# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-28 15:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_movie_filename'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='title_hash',
        ),
        migrations.AddField(
            model_name='movie',
            name='filepath',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='movie',
            name='director',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='movies.Director'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='year',
            field=models.DateTimeField(blank=True, verbose_name='Movie year'),
        ),
    ]
