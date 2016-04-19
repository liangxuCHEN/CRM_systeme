 #-*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect,render_to_response,RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django import forms
from crm.forms import PersonForm, AuthenticationForm, CastleForm
from crm.models import Person, Bill, Castle
from datetime import datetime, timedelta
from tool import send_mail, check_bill_each_day,generate_booking_mail, generate_custome_mail, add_artical_reading
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
        content["form"] = PersonForm()
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

def booking_cave(request):
    if request.method == "POST":
        data=request.POST
        try:
            new_person = Person.objects.get_or_create(
                name=data['clientName'],
                phone=data["phone"],
                sex="M",
                email=data['email'],
                comment=u"visit chateau from " + data['from_site']
            )

            if generate_booking_mail(data):
                content =  u"<p>您好%s</p><h4>我们已经收到您的预约信息，行程顾问会尽快回复您, 谢谢</h4>"  % data['clientName']
            else:
                content =  u"<p>您好%s</p><h4>我们非常抱歉，您的预约没有成功，请直接联系%s</h4>"  % (data['clientName'], data['service_phone'])
        except:
           content =  u"<p>您好%s</p><h4>我们非常抱歉，您的预约没有成功，请直接联系%s</h4>"  % (data['clientName'], data['service_phone'])
        
        return HttpResponse(content)
    
    try:
        site = request.GET["site"]
        service_phone = request.GET["service_phone"]
    except:
        site = u"客服电话"
        service_phone = "400-845-0085"

    content ={
       "from_site" : site,
       "service_phone" : site + u"客服 : "+ service_phone,
    }
    if "Mobile" in request.META["HTTP_USER_AGENT"]:
        return render(request, "booking_phone.html", content)
    
    return render(request, "booking.html", content)

def custome_travel(request):
    if request.method == "POST":
        data=request.POST
        try:
            new_person = Person.objects.get_or_create(
                name=data['clientName'],
                phone=data["phone"],
                sex="M",
                email=data['email'],
                comment=u"custome travel from " + data['from_site']
                )

            if generate_custome_mail(data):
                content =  u"<p>您好%s</p><h4>我们已经收到您的定制信息，行程顾问会尽快回复您,谢谢</h4>"  % data['clientName']
            else:
                content =   u"<p>您好%s</p><h4>我们非常抱歉，您的预约没有成功，请直接联系%s</h4>"  % (data['clientName'], data['service_phone'])
        except:
           content =   u"<p>您好%s</p><h4>我们非常抱歉，您的预约没有成功，请直接联系%s</h4>"  % (data['clientName'], data['service_phone'])
        return HttpResponse(content)
    
    try:
        site = request.GET["site"]
        service_phone = request.GET["service_phone"]
    except:
        site = u"客服电话"
        service_phone = "400-845-0085"

    content ={
       "from_site" : site,
       "service_phone" : site + u"客服 : "+ service_phone,
    }
    return render(request, "custome.html", content)

def castle(request):
    content = {}
    castles =Castle.objects.all()
    if  request.GET != {}:
        name = request.GET.get('name', '')
        city = request.GET.get("city", "")
        open_sun = request.GET.get("open_sun", "")
        open_sat = request.GET.get("open_sat", "")
        level = request.GET.get("level", "")
        if name != '':
            castles = castles.filter(name__contains=name)
        if city !="":
            castles = castles.filter(city=city)
        if level !="":
            castles = castles.filter(level=level)
        if open_sun !="":
            castles = castles.filter(open_sun=open_sun)
        if open_sat !="":
            castles = castles.filter(open_sat=open_sat)

    content["form"] = CastleForm(auto_id=False)
    page_size =  10
    paginator = Paginator(castles, page_size)
    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1
    try:
        castle_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        castle_page = paginator.page(paginator.num_pages)

    content["castles"] = castle_page
    return render(request, "castle.html", content)

def addCastleView(request):
    if request.method == 'POST':
        form = CastleForm(data=request.POST)
        content = {}
        if form.is_valid():
            form.save()
            return redirect('/castle')
        else:
            content['form'] = CastleForm()
            content['info'] = u"未能保存,请再次填写表格"
            return render(request, 'castle.html', content)
    else:
        form = CastleForm()

    return render_to_response('castle.html', {'form': form,},
        context_instance=RequestContext(request))

def add_reading(request):
    if request.user.is_authenticated():
        num = request.GET.get('num')
        url = request.GET.get('url')
        if num==None or url==None:
            return render(request, "script.html")
        else:
            resp = StreamingHttpResponse(add_artical_reading(num, url))
            return resp
    else:
         return HttpResponseRedirect('/login')
