# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-10-23 12:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0007_chateau_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='chateau',
            name='pic_url',
            field=models.URLField(blank=True, null=True, verbose_name='\u56fe\u7247URL'),
        ),
    ]
