# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-19 03:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0009_auto_20180919_0246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='piece',
            name='artists',
            field=models.ManyToManyField(blank=True, to='viewer.Artist'),
        ),
    ]