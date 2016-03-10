 #-*- coding: utf-8 -*-
#from xlwt import Workbook
import datetime
import email
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
import email.Encoders as encoders
from crm.models import Person, Bill
from weather import get_three_days_weather

SMTP_SERVER = 'smtp.163.com'
MAIL_FROM = 'chenliangxu68@163.com'
PW = '163$323428'


def send_mail(mail_to, subject, msg_txt):
    # Record the MIME types of both parts - text/plain and text/html.
    msg = MIMEText(msg_txt, 'html', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = MAIL_FROM
    msg['To'] = mail_to
    server = smtplib.SMTP(SMTP_SERVER, 25)
    try:
        server.login(MAIL_FROM, PW)
        mailto_list = mail_to.strip().split(",")
        if len(mailto_list) > 1:
            for mailtoi in mailto_list:
                server.sendmail(MAIL_FROM, mailtoi.strip(), msg.as_string())
        else:
            server.sendmail(MAIL_FROM, mail_to, msg.as_string())
    except:
        server.quit()
        return False

    server.quit()
    return True

def check_bill_each_day(bills):
    num = len(bills)
    body = u"<p>今天有%d个邮件提醒需要发送,他们明天就要出发旅游</p><br><br>" % (num)
    if(num > 0):
        for bill in bills:
            body += generate_bill_body(bill)

    mail_to = 'lchen@europely.com,reservation@europely.com'
    res = send_mail(mail_to, u"明天出行订单提醒", body)
    if not res:
        return u'<p id="info">邮件放送不成功, <a href="http://112.74.109.3:4040">请查看订单情况</a></p>'
    return u'<p id="info">邮件放送成功</p>'

def generate_bill_body(bill):
    bill_body =u"<hr>"
    city = bill.city or 'Paris,France'
    bill_body += u"<p>客人 : %s , 邮箱 : %s, 旅游目的地:%s: </p>"  % (bill.person.name, bill.person.email, city)
    bill_body += u"订单备注: %s" % bill.comment
    bill_body += get_three_days_weather(city=city) + u"<hr><br>"
    bill.is_send_wether = True
    bill.save()
    return bill_body

def generate_booking_mail(data):
    body = u"<p>来自 %s 网站的咨询, 有一个客户的预约 <br>" % data['from_site']
    body += u'姓名:  ' + data['clientName'] + '<br>'
    body += u'电话:  ' + data['phone'] + '<br>'
    body += u'邮箱:  ' + data['email']+ '<br>'
    body += u'参观日期:  ' + data['visitDate'] + '<br>'
    body += u'参观酒庄:  ' + get_list(data.getlist("caveName")) + '<br>'
    body += u'参观人数:  ' + data['member'] + '<br>'
    body += u'儿童:  ' + data['has_child'] + '<br>'
    body += u'留言: ' + data['commentText'] + '<br></p>'
    mail_to = 'lchen@europely.com,reservation@europely.com'
    res = send_mail(mail_to, u"酒庄预约咨询", body)
    return res

def generate_custome_mail(data):
    body = u"<p>来自 %s 网站的咨询, 有一个客户的定制旅游咨询 <br>" % data['from_site']
    body += u'姓名:  ' + data['clientName'] + '<br>'
    body += u'电话:  ' + data['phone'] + '<br>'
    body += u'邮箱:  ' + data['email']+ '<br>'
    body += u'出发日期:  ' + data['date_begin'] + '<br>'
    body += u'游玩天数:  ' + data['day'] + '<br>'
    body += u'游玩人数:  ' + data['num'] + '<br>'
    body += u'目的地:  ' + data['place'] + '<br>'
    body += u'特殊需求: ' + data['comment'] + '<br></p>'
    mail_to = 'lchen@europely.com,reservation@europely.com'
    res = send_mail(mail_to, u"定制旅游咨询", body)
    return res

def get_list(data):
    s = u""
    for x in data:
        s += x + " ; "
    return s