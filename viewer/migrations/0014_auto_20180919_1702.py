# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-19 17:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0013_auto_20180919_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='piece',
            name='graphics_format',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
