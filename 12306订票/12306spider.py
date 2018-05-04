#!usr/bin/env python
# -*- coding: utf-8 -*-
#_Author:shenshi
#date:2018/5/2 22:01
from . station import  stationDict
import requests
import urllib
from urllib import  parse
#自己在这个模块里面填写字节用户名和密码
from .user import username,pwd
import time
import re
import random

USER_AGENTS = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

def getHeader():
    header=USER_AGENTS
    length=len(header)
    Header=header[random.randint(1,length-1)]
    return  Header


headers = {'User-Agent':getHeader()}

# 使用seesion就不用生成cookie对象来维持了
s = requests.Session()

#登陆模块
def login():


    # 验证码图片地址并将他写入本地
    code_url='https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.16282029820909516'
    code_req=s.get(code_url,headers=headers)
    #以2进制写入本地
    with open('code.png', 'wb') as fn:
        fn.write(code_req.content)
    #验证码网址
    captcha_url='https://kyfw.12306.cn/passport/captcha/captcha-check'
    code = input('请输入验证码所对应的坐标：')
    data1 = {
        'login_site': 'E',
        'answer': code,
         'rand': 'sjrand'
    }
    code_req=s.post(captcha_url,data=data1,headers=headers)

    #登陆网址
    url="https://kyfw.12306.cn/passport/web/login"
    data2={
         'username': username,
         'password': pwd,
         'appid': 'otn'
    }
    req=s.post(url,data=data2,headers=headers).json()
    #如果登陆成功的话code的值为0
    if req['result_code'] == 0:
        print('登陆成功')
        userlogin_url = 'https://kyfw.12306.cn/otn/login/userLogin'
        data = {
            '_json_data': ''
        }
        userlogin_req = s.post(userlogin_url, data=data, headers=headers)

        userlogin_url2 = 'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin'
        userlogin_req = s.get(userlogin_url2, headers=headers)
        uamtk_url='https://kyfw.12306.cn/passport/web/auth/uamtk'

        data={
            'appid': 'otn'
        }
        uamtk_req= s.post(uamtk_url,data=data,headers=headers).json()
        tk=uamtk_req['newapptk']
        uamauth_url='https://kyfw.12306.cn/otn/uamauthclient'
        data3={
             'tk':tk
        }
        uamauth_req=s.post(uamauth_url,data=data3,headers=headers).json()


        userlogin_url = 'https://kyfw.12306.cn/otn/login/userLogin'
        userlogin_req = s.get(userlogin_url, headers=headers)

        #验证是否登陆成功
        init_url='https://kyfw.12306.cn/otn/index/initMy12306'
        init_html=s.get(init_url,headers=headers).text
        print('登陆成功，正在初始化页面，下面准备查询')
        print('++++++++++++++++++++++')
        print(init_html)

    else:
        print('验证码错误，请重新验证···')
        time.sleep(3)
login()

def check():
    # 出发时间：
    global train_date
    train_date = input('请输入出发日期（格式如2018-05-04）：')

    # 出发城市：
    global fromStation
    fromStation = input('填写出发地：')
    from_station = stationDict[fromStation]

    # 到达城市：to
    global toStation
    toStation = input('填写目的地：')
    to_station = stationDict[toStation]

    #检查余票
    check_url='https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT'%(train_date,from_station,to_station)
    check_req=s.get(check_url,headers=headers).json()
    return check_req['data']['result']


# [3]=车次 [8]=出发时间 [9]=到达时间 [10]=历时时间  [21]高级软卧 [23]=软卧  [26]=无坐  [28]=硬卧 [29]=硬座
# 【30】=二等座 【31】=一等座  【32】=特等座  【33】=动卧
'''
[3]=车次
[8]=出发时间
[9]=到达时间
[10]=历时时间
[21]=高级软卧
[23]=软卧
[26]=无坐
[28]=硬卧
[29]=硬座
[30]=二等座
[31]=一等座 
[32]=特等座
[33]=动卧
'''
#索引为0
index=0
for i in check():
    #通过|切片
    tmplist = i.split('|')
    # for i in tmplist:
    #     #打印出每个i以及对应的索引值
    #     print(index,i)
    #     index+=1

#捕捉下错误
try:
    #如果二等票=有或者这个的数字大于0证明有篇：
    if tmplist[30] == '有' or int(tmplist[23]) > 0:
        print('''
          该车次有二等座票
        -------------------------
          车次: %s
          出发时间: %s
          到达时间: %s
          历时时间: %s
          余票: %s
        -------------------------
          ''' % (tmplist[3], tmplist[8], tmplist[9], tmplist[10], tmplist[23]))

except Exception as e:
    print(e)


def order():
    #预定的第一个url，检查用户
    checkUser_url='https://kyfw.12306.cn/otn/login/checkUser'
    data={
        '_json_data': ''
    }
    checkUser_req=s.post(checkUser_url,data=data,headers=headers)
 #提交订单的请求
    submit_url='https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
    data = {
        #对这个str进行格式的解码，转为无%号的格式
        'secretStr':urllib.parse.unquote(tmplist[0]),
        'train_date': train_date,
        'back_train_date': '2018 - 05 - 04',
        'tour_flag': 'dc',
        'purpose_codes': 'ADULT',
        'query_from_station_name': fromStation,
        'query_to_station_name': toStation
    }
    submit_req=s.post(submit_url,data=data,headers=headers)
    # print(submit_req)

    init_url='https://kyfw.12306.cn/otn/confirmPassenger/initDc'
    data = {
        '_json_att': ''
    }
    init_req=s.post(init_url,data=data,headers=headers).content.decode('utf8')

    #正则匹配规则
    globalRepeatSubmitToken = re.findall(r"globalRepeatSubmitToken'='(.*?)'")[0]
    key_check_isChange = re.findall(r"key_check_isChange'='='(.*?)'")[0]
    # print(globalRepeatSubmitToken)
   #确认url
    confirm_url='https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
    data = {
        '_json_att': '',
        'REPEAT_SUBMIT_TOKEN': globalRepeatSubmitToken
    }
    checkOrder_url='https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
    data={
        'cancel_flag': '2',
        'bed_level_order_num': '000000000000000000000000000000',
        'passengerTicketStr': ('O, 0, 1, 你的名字, 1, 你的身份证号,, N'),
        'oldPassengerStr': ('你的名字, 1, 你的身份证号, 1_'),
        'tour_flag': 'dc',
        'randCode': '',
        'whatsSelect': '1',
        '_json_att': '',
        'REPEAT_SUBMIT_TOKEN': globalRepeatSubmitToken
         }
    checkOrder_req=s.post(checkOrder_url,data=data,headers=headers)
    #提交订单：
    confirmPassenger_url='https://kyfw.12306.cn/otn/confirmPassenger/'

    data = {
        'passengerTicketStr': ('座位类型, 0, 1, 名字, 1, 身份证号,, N'),
        'oldPassengerStr': ('名字, 1, 身份证号, 1'),
        'tour_flag': 'dc',
        'randCode': '',
        'purpose_codes': '00',
        'key_check_isChange': key_check_isChange,
        'train_location': '',
        'choose_seats': '',
        'seatDetailType': '000',
        'roomType': '00',
        'dwAll': 'N',
        '_json_att': '',
        'REPEAT_SUBMIT_TOKEN': globalRepeatSubmitToken

    }
    confirmPassenger_req=s.post(confirmPassenger_url,data=data,headers=headers)
    print(confirmPassenger_req)

order()

