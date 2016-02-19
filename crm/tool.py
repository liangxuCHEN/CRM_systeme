 #-*- coding: utf-8 -*-
#from xlwt import Workbook
import datetime
import email
import smtplib

from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
 
from email.MIMEText import MIMEText
import email.Encoders as encoders

SMTP_SERVER = 'smtp.163.com'
MAIL_FROM = 'chenliangxu68@163.com'
PW = 'xxx'


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

#print send_mail('chenliangxu68@163.com', 'lchen@europely.com', 'weather', u"办法是在发送HTML的同时再附加一个纯文本")
