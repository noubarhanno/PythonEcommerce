# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-10 15:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0004_card'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='brnad',
            new_name='brand',
        ),
    ]
