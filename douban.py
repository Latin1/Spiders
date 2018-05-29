# -*- coding:utf-8 -*-
#Author:shenshi
#date:2018/5/29 8:53
import requests
import time

for a in range(498):
    #所有地址
    url_list='https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start={}'.format(a*20)
    req=requests.get(url_list).json()
    time.sleep(2)

    for i in range(20):
        dict=req['data'][i]
        #地址
        url=dict['url']
        #电影名字
        title=dict['title']
        #导演
        director = dict['directors']
        #评分
        rate=dict['rate']
        #演员
        cast=dict['casts']

        INFO='''
        电影：%s
        导演：%s
        演员：%s
        评分：%s
        地址：%s
        '''%(title,director,cast,rate,url)
        print(INFO)