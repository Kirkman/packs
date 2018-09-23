# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-19 17:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0011_auto_20180919_0319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pack',
            name='date',
            field=models.DateField(blank=True),
        ),
        migrations.RemoveField(
            model_name='piece',
            name='artists',
        ),
        migrations.AddField(
            model_name='piece',
            name='artists',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='viewer.Artist'),
            preserve_default=False,
        ),
    ]
