# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-28 11:10
from __future__ import unicode_literals

import demo.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0004_dropzonemodel_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dropzonemodel',
            name='file',
            field=models.FileField(upload_to=demo.models.content_file_name),
        ),
    ]
