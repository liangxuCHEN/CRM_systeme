 #-*- coding: utf-8 -*-
from django.contrib import admin
from crm.models import Person, Bill

# Register your models here
class PersonAdmin(admin.ModelAdmin):
    list_display = ('phone', 'name', 'comment')
    fields = ('phone', 'name', 'sex','email','comment')

class BillAdmin(admin.ModelAdmin):
    list_display = ('travel_date','comment')

admin.site.register(Person, PersonAdmin)
admin.site.register(Bill, BillAdmin)