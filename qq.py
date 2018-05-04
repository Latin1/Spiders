#!usr/bin/env python
# -*- coding: utf-8 -*-
#_Author:shenshi
#date:2018/5/5 0:25
import requests
import time, random

# 请使用抓包后填写以下数据
# cookie的值
cookie = ''
# pic_id可以自己抓包获取，我这里提供一个id
pic_id = '175'
bkn = ''  # bkn
groups = ['']  # qq群号，可以为多个群号

num = len(groups)

url = 'https://qun.qq.com/cgi-bin/qiandao/sign/publish'


def geta(a, t, p):
    count = 1
    while count <= num:
        for gc in groups:
            headers = {
                'Cookie': cookie,
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A365 Safari/600.1.4'
            }
            data = {
                'client': '2',

                'gallery_info': {"category_id": 21, "page": 0, "pic_id": pic_id},
                'gc': gc,
                'lgt': '1',
                'poi': p ,
                'pic_id':'',
                'template_id': a,
                'bkn': bkn,
                'text': t,
                'lat': '0',
                'template_data': ''
            }
            r = requests.post(url=url,data=data, headers=headers,verify=False).json()
            data=r['data']['sign_id']
            if data.isdigit():
                print('签到成功')
            else:
                print('签到失败')
            time.sleep(4)
            count = count + 1


a = random.randint(0, 10)
t = input('请输入你要输入的文字：')
p = input('请输入自定义定位地址：')
geta(a, t, p)
