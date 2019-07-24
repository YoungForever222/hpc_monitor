import os
import re
import smtplib
from email.mime.text import MIMEText
import time
import datetime
def sleeptime(hour,min,sec):
    return hour*3600 + min*60 + sec
def monitor(firstname,nodenames,threshold=55):
    # Get the record time
    Day = datetime.datetime.now().strftime('%Y-%m-%d')
    nowTime=datetime.datetime.now().strftime('%H')
    nowTimeDate=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logName = "./log/Temperature"+Day
    # Information of the email
    #发送人
    msg_from='1005636583@qq.com'  
    passwd='bjxbauztltwhbbgg'             
    #接受人
    #msg_to=['yu222@mail.ustc.edu.cn','song2016@mail.ustc.edu.cn']
    msg_to=['yu222@mail.ustc.edu.cn']
    subject1="【多尺度复杂流动实验室】机房温度提示"
    subject2="【多尺度复杂流动实验室】机房超温警报！！！"
    content = 'Now time is '+nowTimeDate+'\n'
    # One record text per day
    if not os.path.exists(logName):
        with open(logName+'.csv','w') as f:
            f.write("time,node,max_temp\n")
    # For each node
    max_temperature = []
    for nodename in nodenames:
        cmdline = 'pdsh -w '+firstname+nodename+' sensors'
        print(cmdline)
        sensors = os.popen(cmdline).read()
        sensors = re.sub('\s','',sensors)
        print(sensors)
        temperature = []
        #取出所有内核温度
        for i in sensors.split(firstname+nodename+':Core'):
            for j in i.split('('):
                print(j)
                if j[0] not in ['a','c','i','h','n']:
                    temperature.append(j[-7:-3])
        #取出最大内核温度
        temp = max(temperature)
        #print(temperature)
        max_temperature.append(temp[1:3])
        #print(temp[1:3])
        #print(max_temperature[1:-1])
        if int(temp[1:3]) > threshold :
            content+= 'IP is 192.168.211.1'+nodename+'\t'        \
                +'The temperature is ' + temp +'\n'
        #写log文件
        with open(logName+'.csv', "a") as f:
            f.write(nowTimeDate+','+firstname+nodename+','+temp[1:3]+'\n')
    # 定时提醒
    if datetime.datetime.now().strftime('%H') in ['0','3','6','9','12','18','21']:
        msg = MIMEText(content)
        msg['Subject'] = subject1
        msg['From'] = msg_from
        for i in range(len(msg_to)):
            msg['To'] = msg_to[i]
            try:
                s = smtplib.SMTP_SSL("smtp.qq.com",465)
                s.login(msg_from, passwd)
                s.sendmail(msg_from, msg_to[i], msg.as_string())
            finally:
                s.quit()
    # 超温报警
    if int(max(max_temperature)) > threshold :
        content  += 'WARMING! The temperature is too HIGH!!!\n'
        msg = MIMEText(content)
        msg['Subject'] = subject2
        msg['From'] = msg_from
        for i in range(len(msg_to)):
            msg['To'] = msg_to[i]
            try:
                s = smtplib.SMTP_SSL("smtp.qq.com",465)
                s.login(msg_from, passwd)
                s.sendmail(msg_from, msg_to[i], msg.as_string())
            finally:
                s.quit()
    return logName+'.csv'
    
