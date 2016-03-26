# -*- condig:utf-8 -*-
import time
import csv
import smtplib
import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def creatFile():
    timeNow = time.strftime("%Y-%m-%d-%H-%M-%S")
    csvFileName = timeNow + ".csv"
    with open(csvFileName,"w",newline='') as cvsFile:
        spamwriter = csv.writer(cvsFile)
        spamwriter.writerow([u'门店'] + [u'设备'] + ['sn'] +[u'型号']  + [u'版本号'] +[u'最后连接时间']+[u'日志链接'])
    return csvFileName

def cvsWrite(msg,csvFileName):
    with open(csvFileName,"a+",newline='') as cvsFile:
        spamwriter = csv.writer(cvsFile)
        lists = [msg]
        spamwriter.writerows(lists)

def cvsFileSend(cvsFileName):
    print(cvsFileName)
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = u'设备每日异常报表'
    att = MIMEText(open(cvsFileName, 'r').read(), 'base64', 'utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename='+ cvsFileName + "\'"
    msgRoot.attach(att)

    smtp = smtplib.SMTP()
    smtp.connect('smtp.exmail.qq.com')
    smtp.login(config.emailConfig['username'], config.emailConfig['password'])
    smtp.sendmail(config.emailConfig['sender'], config.emailConfig['receiver'], msgRoot.as_string())
    smtp.quit()