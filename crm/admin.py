 #-*- coding: utf-8 -*-
from django.contrib import admin
from crm.models import Person, Bill, Castle

# Register your models here
class PersonAdmin(admin.ModelAdmin):
    list_display = ('phone', 'name', 'comment')
    fields = ('phone', 'name', 'sex','email','comment')

class BillAdmin(admin.ModelAdmin):
    list_display = ('travel_date', 'person','comment')

class CastleAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'url', 'open_sun', 'open_sat', 'level')

admin.site.register(Person, PersonAdmin)
admin.site.register(Bill, BillAdmin)
admin.site.register(Castle, CastleAdmin)