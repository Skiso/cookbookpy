# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-24 10:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cookbook', '0003_commentaire_recette'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recette',
            name='user',
            field=models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, related_name='id_user', to=settings.AUTH_USER_MODEL),
        ),
    ]