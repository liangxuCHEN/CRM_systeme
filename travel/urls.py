"""travel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from crm import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^login$', views.LoginView, name='login'),
    url(r'^logout$', views.LogoutView, name='logout'),
    url(r'^bill$', views.bill_index, name='bill_index'),
    url(r'^person$', views.person_index, name='person_index'),
    url(r'^add_person$', views.add_person, name='add_person'),
    url(r'^add_bill$', views.add_bill, name='add_bill'),
    url(r'^check_bill$', views.check_bill, name='check_bill'),
    url(r'^booking_cave/$', views.booking_cave, name='booking_cave'),
    url(r'^custome/$', views.custome_travel, name='custome_travel'),
    url(r'^castle/$', views.castle, name='castle'),
    url(r'^addCastleView/$', views.addCastleView, name="addCastleView"),
    url(r'^add_reading/$',views.add_reading, name='add_reading'),
    url(r'^upload_pic/$',views.upload_pic, name='upload_pic'),
    url(r'^create_qiniu_token/$',views.create_qiniu_token, name='create_qiniu_token'),
    url(r'^download_pic/$',views.download_pic, name='download_pic'),
    url(r'^get_qiniu_file/$',views.get_qiniu_file, name='get_qiniu_file'),
    url(r'^contract/$',views.contract, name='contract'),
    url(r'^make_contract/(?P<contract_id>\d+)/$',views.make_contract, name='make_contract'),
]
