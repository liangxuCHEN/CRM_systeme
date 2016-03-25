 #-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

CITY_MODEL = (
    ('Paris,France', u'巴黎'),
    ('Reims,France', u'兰斯'),
    ('Dijon,France', u'第戎'),
    ('Tour,France', u'图尔'),
    ('Bordeaux,France', u'波尔多'),
    ('Avignon,France', u'阿维尼翁'),
    ('Nice,France', u'尼斯'),
    ('Marseille,France', u'马赛'),
    ('Roman,Italy', u'罗马'),
    ('Milan,Italy', u'米兰'),
    ('Geneva,Switzerland', u'日内瓦'),
    ('Prague,Czekh', u'布拉格'),
)

LEVEL_BOOK = (
    (u'非常容易', u"非常容易"),
    (u"容易", u"容易"),
    (u"一般", u"一般"),
    (u"困难", u"困难"),
    (u"几乎不可能", u"几乎不可能"),
)
# Create your models here.
class Person(models.Model):
    def __unicode__(self):
        return self.name
    SEX_MODEL = (
        ('M', u'先生'),
        ('W', u'女士'),
    )
    name = models.CharField(u"姓名", max_length = 60)
    email = models.EmailField(u"邮箱")
    phone = models.CharField(u"电话", max_length = 20)
    sex = models.CharField(max_length = 1, choices = SEX_MODEL)
    comment = models.CharField(u"备注", max_length = 200, null = True, blank = True)

class Castle(models.Model):
    name = models.CharField(u"名字", max_length=60)
    url = models.URLField(u"官网",null = True, blank = True)
    city = models.CharField(u"目的地", max_length=15, choices = CITY_MODEL, blank = True, null = True)
    comment = models.TextField(u"备注")
    open_sun = models.BooleanField(u"周日开门", default=False)
    open_sat = models.BooleanField(u"周六开门", default=False)
    level = models.CharField(u"预约难度", max_length=15, choices = LEVEL_BOOK, blank = True, null = True)

class Bill(models.Model):
    person = models.ForeignKey(Person)
    travel_date = models.DateField(u"出发日期")
    city = models.CharField(u"旅游目的地", max_length=15, choices = CITY_MODEL, blank = True, null = True)
    is_send_wether = models.BooleanField(u"已发天气提醒", default=False)
    is_send_plan = models.BooleanField(u"已发行程提醒", default=False)
    comment = models.CharField(u"备注", max_length = 200, null = True, blank = True)