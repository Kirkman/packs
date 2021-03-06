# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-18 19:54
from __future__ import unicode_literals

from django.db import migrations, models
import viewer.models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0007_auto_20180918_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='country',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='artist',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='artist',
            name='profile_photo',
            field=models.ImageField(blank=True, upload_to=viewer.models.get_profile_image_path),
        ),
        migrations.AlterField(
            model_name='group',
            name='about',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='group',
            name='date_founded',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='header_photo',
            field=models.ImageField(blank=True, upload_to=viewer.models.get_profile_image_path),
        ),
        migrations.AlterField(
            model_name='group',
            name='website',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
