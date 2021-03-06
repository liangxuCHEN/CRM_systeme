# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-10-23 11:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_contract'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chateau',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='\u6cd5\u8bed\u540d\u5b57')),
                ('cn_name', models.CharField(max_length=80, verbose_name='\u4e2d\u6587\u540d\u5b57')),
                ('presentation_chateau', models.TextField(blank=True, null=True, verbose_name='\u9152\u5e84\u4ecb\u7ecd')),
                ('presentation_vin', models.TextField(blank=True, null=True, verbose_name='\u7ea2\u9152\u4ecb\u7ecd')),
                ('place', models.CharField(max_length=80, verbose_name='\u4f4d\u7f6e')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, verbose_name='\u670d\u52a1\u540d\u79f0')),
                ('description', models.CharField(blank=True, max_length=200, null=True, verbose_name='\u670d\u52a1\u63cf\u8ff0')),
                ('price', models.IntegerField(verbose_name='\u6bcf\u4eba\u8d39\u7528\u20ac')),
                ('chateau', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Chateau')),
            ],
        ),
    ]
