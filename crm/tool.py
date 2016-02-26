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
    body = u"<p>今天有%d邮件提醒需要发送,他们明天就要出发旅游</p><br><br>" % (num)
    if(num > 0):
        for bill in bills:
            body += generate_bill_body(bill)

    mail_to = 'lchen@europely.com'
    res = send_mail(mail_to, u"明天出行订单提醒", body)
    if not res:
        return u'<p id="info">邮件放送不成功, <a href="http://112.74.109.3:4040">请查看订单情况</a></p>'
    return u'<p id="info">邮件放送成功</p>'

def generate_bill_body(bill):
    bill_body =u"<hr>"
    city = bill.city or 'Paris,France'
    bill_body += u"<p>客人 : %s , 邮箱 : %s, 旅游目的地:%s明天的天气情况: </p>"  % (bill.person.name, bill.person.email, city)
    bill_body += u"订单备注: %s" % bill.comment
    bill_body += get_three_days_weather(city=city) + u"<hr><br>"
    bill.is_send_wether = True
    bill.save()
    return bill_body

#print send_mail('chenliangxu68@163.com', 'lchen@europely.com', 'weather', u"办法是在发送HTML的同时再附加一个纯文本")
