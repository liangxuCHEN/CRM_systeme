#-*- coding: utf-8 -*-
#from xlwt import Workbook
import datetime
import smtplib
import httplib2
import logging
import os
import settings
import qiniu.config
from crm.models import Person, Bill
from email.MIMEText import MIMEText
from random import Random
from qiniu import Auth, put_file, etag, urlsafe_base64_encode, BucketManager
from weather import get_three_days_weather

def log_init(model="", file_name=""):
    today = datetime.datetime.now()
    time_tmp = str(today).split(" ")
    timestamp = time_tmp[0]+"_"+time_tmp[1].split(".")[0]+"_"
    
    if (model == "a"):
        if not os.path.isfile("log-txt/"+file_name+".txt"):
            model = "w"
            file_name = timestamp + file_name
    else:
         model = "w"
         file_name = timestamp + file_name
    logging.basicConfig(
        filename=os.path.join(os.getcwd(), "log-txt/"+file_name+".txt"),
        level=logging.INFO,
        filemode=model,
        format='%(asctime)s - %(levelname)s: %(message)s'
    )
    return logging

def send_mail(mail_to, subject, msg_txt):
    # Record the MIME types of both parts - text/plain and text/html.
    msg = MIMEText(msg_txt, 'html', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = settings.MAIL_FROM
    msg['To'] = mail_to
    server = smtplib.SMTP(settings.SMTP_SERVER, 25)
    try:
        server.login(settings.MAIL_FROM, settings.PW)
        mailto_list = mail_to.strip().split(",")
        if len(mailto_list) > 1:
            for mailtoi in mailto_list:
                server.sendmail(settings.MAIL_FROM, mailtoi.strip(), msg.as_string())
        else:
            server.sendmail(settings.MAIL_FROM, mail_to, msg.as_string())
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
    #mail_to = 'lchen@europely.com'
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

def add_artical_reading(num, url):
    log = log_init(model="a", file_name="add_reading_log")
    log.info("/******misson is  adding " + num + " time for the artical*****/")
    log.info(url)
    yield u"<html><body><h2>程序开始运行，需要一点时间完成，请耐心等待</h2>\n"
    h = httplib2.Http()
    for x in range(0,int(num)):
        res,content = h.request(url, "GET")
        if res['status'] == '200':
            yield u"<p>成功增加一次浏览</p>"
    yield u'<h2>完成,请查看帖子</h2><a href="%s">点击这里</a></body></html>\n' % url
    log.info("/*******misson is finished********/")
    log.close()

def qiniu_token(file_name):
    #构建鉴权对象
    q = qiniu_q()
    #要上传的空间
    bucket_name = 'love-travel'
    #上传到七牛后保存的文件名
    key =  file_name.encode("utf-8")
    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    return {"token" : token, "key" : key}

def qiniu_upload(token, key, pic):
    #res = qiniu_token(file_name)
    ret, info  = put_file(token, key, pic)
    if  ret['key'] == key:
        return {"result" : True, "file_name" :  key}
    else:
        return {"result" : False, "file_name" :  ""}

def qiniu_download(data):
    #构建鉴权对象
    q = qiniu_q()
    #上传的空间
    bucket_domain = settings.BUCKET_DOMAIN
    # generate key
    if data["url"] == "diy_url":
        logo_url = urlsafe_base64_encode(data["diy_url"])
    else:
        logo_url = urlsafe_base64_encode(data["url"])
   
    key ="?imageView2/1/w/%d/h/%d/q/%d/format/%s|watermark/1/image/%s/dissolve/%d/gravity/%s/dx/30/dy/30" % (
        int(data["width"]),
        int(data["height"]),
        int(data["quality"]),
        data['format'],
        logo_url,
        int(data["dissolve"]),
        data["place"],
    )
    key = data["key"]+key
    #有两种方式构造base_url的形式
    base_url = 'http://%s/%s' % (bucket_domain, key)
    #可以设置token过期时间
    private_url = q.private_download_url(base_url, expires=3600)
    h = httplib2.Http()
    res,content = h.request(private_url, "GET")
    if res['status'] == '200':
        return {"result" : True, "private_url" : private_url }
    else:
        return {"result" : False, "private_url" : "" }

def random_str(randomlength=5):
    file_name = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        file_name+=chars[random.randint(0, length)]
    today = datetime.datetime.now()
    file_name = file_name+str(today).split(" ")[0]
    return file_name

def qiniu_q():
    #需要填写你的 Access Key 和 Secret Key
    access_key = settings.QINIU_AK
    secret_key = settings.QINIU_SK
    #构建鉴权对象
    return Auth(access_key, secret_key)

def qiniu_file(pre_text, limit):
    q = qiniu_q()
    bucket = BucketManager(q)
    bucket_name = 'love-travel'
    ret, eof, info = bucket.list(bucket_name, prefix=pre_text, delimiter="/", limit=limit)
    if len(ret["items"]) > 0 :
        return {'result' : True, 'files' : ret["items"]}
    else:
        return {'result' : False}