#!usr/bin/env python
# -*- coding: utf-8 -*-
#_Author:wudi666
#date:2018/4/23 16:50
import requests
import time
from bs4 import  BeautifulSoup
import re

def get_url():
    home_url='http://www.fengchaowu.com/'
    urls = ['http://www.fengchaowu.com/forum-45-{}.html'.format(id) for id in range(1, 24)]
    for url in urls:
        try:
            # 防止对服务器的压力过大，以及为了防止自己的ip被服务器ban
            time.sleep(1)
            response=requests.get(url)
            soup=BeautifulSoup(response.text,'lxml')
            titles=soup.find_all('th', class_="new")
            title= BeautifulSoup(str(titles),'lxml')
            a= title.find_all('a',class_='s xst')
            for each in a:
                url=home_url+each.get('href')
                html = requests.get(url).text
                pattern = re.compile("\>http.*rar")
                link = re.findall(pattern, html)[0]
                print(each.string)
                with open('fengchaowu.txt', 'a',encoding='utf-8')as f:
                    f.write(each.string+ '\n'+link+'\n')
        except Exception as  e:
            print(e)

if __name__=="__main__":
    get_url()








