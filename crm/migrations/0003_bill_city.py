# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-19 12:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_auto_20160218_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='city',
            field=models.CharField(blank=True, choices=[('Nice,France', '\u5c3c\u65af'), ('Paris,France', '\u5df4\u9ece'), ('Bordeaux,France', '\u6ce2\u5c14\u591a'), ('Roman,Italy', '\u7f57\u9a6c')], max_length=15, null=True),
        ),
    ]
