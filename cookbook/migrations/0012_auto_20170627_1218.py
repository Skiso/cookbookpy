# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-27 12:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cookbook', '0011_recetteimage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recetteimage',
            old_name='recipe',
            new_name='recette',
        ),
    ]
