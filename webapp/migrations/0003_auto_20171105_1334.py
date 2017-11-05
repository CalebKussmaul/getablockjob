# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-05 13:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20171105_0816'),
    ]

    operations = [
        migrations.AddField(
            model_name='othelloblackblock',
            name='ignorehorizontal',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='othelloblackblock',
            name='ignorevertical',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='othellowhiteblock',
            name='ignorehorizontal',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='othellowhiteblock',
            name='ignorevertical',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='golblock',
            name='gol_cooldown',
            field=models.IntegerField(default=5),
        ),
    ]