#!/usr/bin/python
# -*- coding: utf-8 -*-
import smtplib,time,feedparser,sys,re,requests
from email.mime.text import MIMEText
from email.header import Header
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')
today = time.strftime("%Y-%m-%d",time.localtime())
day = int(time.strftime("%d",time.localtime()))-1

local = "XX"
#地名，比如"北京"
localcode = "xxxxxxxxx"
#在www.weather.com.cn上查询的网址的数字，比如101010100“
kongge = '\n'+'\n'+"============================================"+'\n'
url = 'http://www.weather.com.cn/weather1d/'+localcode+'.shtml'
geter = "xx@xx.xx"
#收信人，为邮箱。
mail_title = "以下是"+yestoday+"的新闻"

def mailsending(subject,send_message,receivers):
    mail_host = 'smtp.gmail.com'
    mail_user = "xx@xx.xx"
    mail_pass = "xxxxxxxx"
    #填写你自己的邮箱密码。
    sender = 'xx@xx.xx'
    #填写发信人邮箱地址
    message = MIMEText(send_message,'plain','utf-8')
    message['From'] = Header(mail_user,'utf-8')
    message['To'] = Header(receivers,'utf-8')
    message['Subject'] = Header(subject,'utf-8')

    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host,587)
    smtpObj.starttls()
    smtpObj.login(mail_user,mail_pass)
    smtpObj.sendmail(sender,receivers,message.as_string())
    
def makeSoup(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = 'utf-8'
        html = r.text
    except:   
        html = ''
    wstr = ''
    if html == '':
        return '哎呀~今天我也不知道'+local+'的天气了'
    else:
        soup = BeautifulSoup(html,'html.parser')
        soup1 = soup.find_all('li',attrs = {'class':'on'})[1]
        str1 = re.findall(r'>(.*)</',str(soup1))
        b = ''
        try:
            slist = re.findall(r'^(.*)</span>(.*)<i>(.*)$',str1[4])
            for x in range(len(slist[0])):
                b += slist[0][x]
        except:
            b = str1[4]
        if '/' in b:
            b = b.replace('/','-')
        str1[4] = '，'+local+'的温度是'+b
        str1[6] = '，小风风是'+str1[6]
        for i in str1:
            if i != '':
                wstr = wstr +i
        if '雨' in wstr:
            wstr += '，今天别忘记带雨伞哦！'
        wstr = wstr.replace('&lt;','')
        return wstr

def sending(x):
    d = feedparser.parse(x)
    sen = ""
    i = 0
    for e in d.entries:
        if int(e.updated[5:7]) == day or day == 1:
            i = int(i)+1
            sen = sen + '\n'+'\n'+str(i)+"、"+e.title+"，"+e.link+"，"+e.updated[5:-6].replace("（","").replace("）","")+"。"
    sen2 = "以下内容是"+d.feed.title+sen+kongge
    return sen2

weather = "今天是"+makeSoup(url).replace("（","").replace("）","")+kongge

url1 = sending('rss网址')
url2 = sending('rss网址')
url3 = sending('rss网址')
url4 = sending('rss网址')
url5 = sending('rss网址')
#填写Rss地址

mailsending(mail_title,weather+url1+url2+url3+url4+url5,geter)
