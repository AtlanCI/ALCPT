# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-12-18 15:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alcpt', '0002_exam_average_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='q_file',
            field=models.FileField(null=True, upload_to='media'),
        ),
    ]
