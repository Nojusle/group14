# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-31 19:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommendations', '0005_angle2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='angle2',
            name='widgets',
        ),
        migrations.DeleteModel(
            name='Angle2',
        ),
    ]
