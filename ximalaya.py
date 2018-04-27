#!usr/bin/env python
# -*- coding: utf-8 -*-
#_Author:shenshi
#date:2018/4/27 14:06
import requests
from  bs4 import  BeautifulSoup
from lxml import etree
import pymysql
import pymongo
import json
headers={
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
}
def get_url():
    #一共84页
    for id in range(1,85):
        url='http://www.ximalaya.com/dq/{}'.format(id)
        try:
            req=requests.get(url,headers=headers).text
            soup = BeautifulSoup(req, 'lxml')
            for item in soup.find_all('div', class_='albumfaceOutter'):
                #找到音频的名字
                href = item.a['href']
                #每个音频对应的url
                name= item.img['alt']
                parse_url(href,name)
        except Exception as e:
            print(e)
#解析url,获取json的地址
def parse_url(href,name):
    #将获取到的url传入到requests
    response = requests.get(href, headers=headers).text
    # print(response)
    #获取到id
    num_list = etree.HTML(response).xpath('//div[@class="personal_body"]/@sound_ids')[0].split(',')
    # print(name + '频道总共含有{}内容'.format(len(num_list)))
    for id in num_list:
        #解析json
        json_url = 'http://www.ximalaya.com/tracks/{}.json'.format(id)
        html = requests.get(json_url, headers=headers).json()
        m4a_url = html.get('play_path')
        title=html.get('title')
        album_title=html.get('album_title')

    #     print('{}的音频地址{}下载成功'.format(title, m4a_url))
    #     #创建数据库的连接
    #     conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='xmly', charset='utf8')
    #     #创建游标
    #     cursor = conn.cursor()
    #     #插入数据
    #     cursor.execute("insert into tb1(name,title,m4a_url)values('{0}','{1}','{2}');".format(name,title, m4a_url))
    #     #提交数据
    #     conn.commit()
    #     #关闭游标
    #     cursor.close()
    #     #关闭连接
    #     conn.close()

        #Pymongo的连接,这样就可以创建MongoDB的连接对象了。
        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        #创建数据库
        db= client['xmly']
        #创建数据集合
        collection = db['data']
        data = {
            'album_title': album_title,
            'title': title,
            'm4a_url': m4a_url,
            }
        collection.insert_one(data)
        #查询数据
        for i in collection.find():
            print(i)



if __name__=="__main__":
    get_url()