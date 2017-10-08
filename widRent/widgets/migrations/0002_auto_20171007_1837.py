# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-07 18:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('widgets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked', models.BooleanField(db_index=True, default=False)),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='page_likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='widget',
            name='diliked',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='widget',
            name='liked',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='widget',
            name='color',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='widget',
            name='height',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='widget',
            name='title',
            field=models.CharField(db_index=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='widget',
            name='width',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='rating',
            name='widget',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='widgets.Widget'),
        ),
    ]