 #-*- coding: utf-8 -*-
from django import forms
from crm.models import Person, Bill
from django.utils import timezone

class AuthenticationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = ['username', 'password']

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['phone', 'name', 'sex','email','comment']

    def clean(self):
        cleaned_data = self.cleaned_data
        phone = cleaned_data.get('phone')

        if Person.objects.filter(phone=phone).exists():
            self._errors['phone'] = self.error_class(['this phone exists'])  

        return cleaned_data
"""
class BillForm(forms.ModelForm):
    class Meta:
        model = Bill

    def save(self): # create new bill
        if self.data['comment'] == "":
            comment = u"the booking message"
        else:
            comment = self.data['bill_comment']
            new_table=Bill.objects.create(
                person = Person.objects.get(id=self.data['person_id']),
                travel_day = self.data
                comment = comment,
            )
"""