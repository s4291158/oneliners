# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-25 15:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oneliners', '0007_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='liked',
            field=models.BooleanField(default=False),
        ),
    ]
