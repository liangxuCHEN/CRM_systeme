# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-18 13:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('travel_date', models.DateField(auto_now_add=True)),
                ('is_send_wether', models.BooleanField(default=False)),
                ('is_send_plan', models.BooleanField(default=False)),
                ('comment', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('sex', models.CharField(choices=[('M', '\u5148\u751f'), ('W', '\u5973\u58eb')], max_length=1)),
                ('comment', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='bill',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Person'),
        ),
    ]
