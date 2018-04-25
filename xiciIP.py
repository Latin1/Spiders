#!usr/bin/env python
# -*- coding: utf-8 -*-
#_Author:shenshi
#date:2018/4/25 15:33
import requests
import time
from lxml import  etree
from bs4 import  BeautifulSoup
headers = {'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Referer':'http://www.xicidaili.com/nn/'

    }
def  getIp(url):
    # 通过session自动保持Cookie
    Session= requests.Session()
    time.sleep(1)
    try:
        #get请求，并且做好编码
        req=Session.get(url,headers=headers)
        #获得网页信息
        html =req.text
        #使用BeautifulSoup
        soup1=BeautifulSoup(html,'lxml')
        ip1=soup1.find_all(id='ip_list')
        soup2=BeautifulSoup(str(ip1),'lxml')
        info =soup2.table.contents
        # 存储代理的列表
        ip_list = []
        for index in range(len(info)):
            if index % 2 == 1 and index != 1:
                dom = etree.HTML(str(info[index]))
                #获得ip
                ip = dom.xpath('//td[2]')
                #获得端口
                port = dom.xpath('//td[3]')
                #获得协议
                protocol = dom.xpath('//td[6]')
                #把获得到的元素写入到iplist里面

                with open('iplist.txt','a')as f:
                    f.write(protocol[0].text.lower() + '://' + ip[0].text + ':' + port[0].text+'\n')
    except Exception as e:
        print(e)

if __name__=="__main__":
    for page in range(1,2949):
        Allurl =['http://www.xicidaili.com/nn/{}' .format(page)]
        for each in Allurl:
            getIp(each)


