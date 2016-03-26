# -*- conding: utf-8 -*-
import logging
import requests
import re
import math
import statistic
import config
import operationCsv

from multiprocessing import Process, Queue

MSG_QUEUE = Queue()
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - [%(levelname)s] [%(threadName)s] (%(module)s:%(lineno)d) %(message)s", )
deviceStatis = statistic.statistic()
def getLogIn(s):
    mms_url = config.mms_url
    logInData = config.logInData
    headers = config.headers
    data = s.post(url=mms_url,data= logInData,headers=headers,allow_redirects=False)
    if data.status_code == 302 :
        cookie = data.cookies
        device_url = "http://mms.morewifi.com/wifi/index/1/?=&=&keyword=&version=&status=0"
        device_list = s.get(url=device_url,cookies = cookie)
        if device_list.status_code == 200 :
            page_num = getIndexNum(device_list.text)
        return cookie,page_num

def deviceInfo(page,queue):
    mypage_Info = re.findall('<td>(.*?)</td>', page, re.S)
    deviceStatis.totalNum = deviceStatis.totalNum + int(len(mypage_Info)/9)
    queue.put(mypage_Info)

def getIndexNum(page):
    index_num = re.findall("<li><a>...</a></li><li .*?><a href=.*?>(.*?)</a></li>",page,re.S)
    return int(index_num[0])

def getDeviceList(queue,s,cookie,page_num):
    for i in range(1,int(page_num)+1):
        url = config.device_url+str(i)+config.url_connect
        device_list = s.get(url=url,cookies = cookie)
        if device_list.status_code == 200 :
            deviceInfo(device_list.text,queue)

def scadaDevice(queue,s,cookie,page_num,csvFileName):
    while deviceStatis.totalQueueNum < page_num:
        if queue.empty() > 0:
            pass
        else:
            msg = queue.get()
            if msg and deviceStatis.totalQueueNum < page_num :
                deviceStatis.totalQueueNum = deviceStatis.totalQueueNum + 1
                analyzeDevice(msg,csvFileName)
                #print(deviceStatis.totalTestNum,deviceStatis.totalMW200HNum)

def reSearch(pattern, string, flags=0):
    return re.findall(pattern,string,flags)

def analyzeDevice(msg,csvFileName):
    if isinstance(msg,(list,)):
        i= 0
        while (i+1)*9 <=len(msg):
            v = msg[i*9:(i+1)*9]
            i = i +1
            if v[0].lower().find("test") != -1 or v[0].find(u"测试") != -1 or v[1].find("test") != -1 or v[1].rfind(u"测试") != -1:
                deviceStatis.totalTestNum = deviceStatis.totalTestNum + 1
            elif v[3].lower().find("mw200") != -1 or v[3] == '' or v[3].lower().find("ctc") !=-1 or v[3].lower().find("ma100") !=-1:
                deviceStatis.totalMW200HNum = deviceStatis.totalMW200HNum + 1
            else:
                #avilibal data process
                if v[6].find(u"异常") !=-1 :
                    store_info = reSearch('<a href="(.*?)">.*?</a>',v[1],re.S)
                    store_name = reSearch('<a href=".*?">(.*?)</a>',v[1],re.S)
                    store_url = "http://mms.morewifi.com" + str(store_info[0])
                    statistic.exception[0] = store_info = store_name[0] + " " + store_url
                    statistic.exception[1] = reSearch('(.*?) \(ID:.*?', v[0], re.S)[0]
                    statistic.exception[2] = v[2]
                    statistic.exception[3] = v[3]
                    statistic.exception[4] = v[4]
                    statistic.exception[5] = v[5]
                    statistic.exception[6] = "http://mms.morewifi.com/wifi/logs/"+reSearch('.*? \(ID:(.*?)\)', v[0], re.S)[0]
                    operationCsv.cvsWrite(statistic.exception,csvFileName)

if __name__ == '__main__':
    logging.info("start the scada system-->>>")
    s = requests.session()
    cookie,page_num = getLogIn(s)
    logging.info(cookie)
    logging.info(page_num)
    csvFileName = operationCsv.creatFile()
    getDevice = Process(target=getDeviceList,args=(MSG_QUEUE,s,cookie,page_num))
    paraseDevice = Process(target=scadaDevice,args=(MSG_QUEUE,s,cookie,page_num,csvFileName))
    getDevice.start()
    paraseDevice.start()
    getDevice.join()
    paraseDevice.join()
    operationCsv.cvsFileSend("2016-03-25-18-17-11.csv")
    logging.info('end the scada system<<<--')