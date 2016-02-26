 #-*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect,render_to_response,RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django import forms
from crm.forms import PersonForm, AuthenticationForm
from crm.models import Person, Bill
from datetime import datetime, timedelta
from tool import send_mail, check_bill_each_day
# Create your views here.

def home(request):
    if request.user.is_authenticated():
        return render(request, 'index.html')
    else:
        return HttpResponseRedirect('/login')

def person_index(request):
    if request.user.is_authenticated():
        content = {}
        persons = Person.objects.all()

        page_size =  10
        paginator = Paginator(persons, page_size)
        try:
            page = int(request.GET.get('page','1'))
        except ValueError:
            page = 1
        
        try:
            person_page = paginator.page(page)
        except (EmptyPage, InvalidPage):
            person_page = paginator.page(paginator.num_pages)

        content['person_list'] = person_page
        return render(request, 'person.html', content)
    else:
        return HttpResponseRedirect('/login')

def bill_index(request):
    if request.user.is_authenticated():
        content = {}
        bills = Bill.objects.all()

        page_size =  10
        paginator = Paginator(bills, page_size)
        try:
            page = int(request.GET.get('page','1'))
        except ValueError:
            page = 1
        
        try:
            bill_page = paginator.page(page)
        except (EmptyPage, InvalidPage):
            bill_page = paginator.page(paginator.num_pages)

        content['bill_list'] = bill_page
        return render(request, 'bill.html', content)
    else:
        return HttpResponseRedirect('/login')

def person_detail(request, person_id):
    if request.user.is_authenticated():
        content = {}
        person = Person.objects.get(id=person_id)
        content['person'] = person
        return render(request, 'person_detail', content) 
    else:
        return HttpResponseRedirect('/login')

def add_person(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            data = request.POST
            form = PersonForm(data)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('person')
            else:
                return render(request, 'add_person.html', {"form" : form})
        else:
            form = PersonForm()
            return render(request, 'add_person.html', {"form" : form})
    else:
        return HttpResponseRedirect('/login')

def add_bill(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            data = request.POST
            person = Person.objects.get(id=data['person_id'])
            if person:
                new_bill=Bill.objects.create(
                    person = person,
                    travel_date = data['travel_date'],
                    comment = data['comment'],
                )
                return HttpResponseRedirect('/bill')
    else:
        return HttpResponseRedirect('/login')

def LoginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        content = {}
        if form.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                content['info'] = u"帐号或密码错误"
                content['form'] = AuthenticationForm()
                return render(request, 'login.html', content)
    else:
        form = AuthenticationForm()

    return render_to_response('login.html', {
            'form': form,
        }, context_instance=RequestContext(request))

def LogoutView(request):
    logout(request)
    return redirect('/')

def check_bill(request):
    content = {}
    bills = Bill.objects.filter(travel_date=datetime.today()+timedelta(1))
    content['weather_info'] = check_bill_each_day(bills)
    return HttpResponse(content['weather_info'])


