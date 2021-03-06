# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-12-12 09:41
from __future__ import unicode_literals

from django.db import migrations, models
import products.models
import storages.backends.s3boto3


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_auto_20181208_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productfile',
            name='file',
            field=models.FileField(storage=storages.backends.s3boto3.S3Boto3Storage(location='protected'), upload_to=products.models.upload_product_file_loc),
        ),
    ]
