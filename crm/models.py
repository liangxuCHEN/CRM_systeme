 #-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Person(models.Model):
    SEX_MODEL = (
        ('M', u'先生'),
        ('W', u'女士'),
    )
    name = models.CharField(max_length = 60)
    email = models.EmailField()
    phone = models.CharField(max_length = 20)
    sex = models.CharField(max_length = 1, choices = SEX_MODEL)
    comment = models.CharField(max_length = 200, null = True, blank = True)

class Bill(models.Model):
    CITY_MODEL = (
        ('Nice,France', u'尼斯'),
        ('Paris,France', u'巴黎'),
        ('Bordeaux,France', u'波尔多'),
        ('Roman,Italy', u'罗马'),
    )
    person = models.ForeignKey(Person)
    travel_date = models.DateField()
    city = models.CharField(max_length=15, choices = CITY_MODEL, blank = True, null = True)
    is_send_wether = models.BooleanField(default=False)
    is_send_plan = models.BooleanField(default=False)
    comment = models.CharField(max_length = 200, null = True, blank = True)