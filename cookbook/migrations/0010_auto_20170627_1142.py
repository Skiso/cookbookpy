# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-27 11:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cookbook', '0009_auto_20170627_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='note',
            field=models.IntegerField(default=0, verbose_name='Note de la recette'),
        ),
    ]
