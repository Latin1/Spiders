# -*- coding: utf-8 -*-
#_Author:www.haofun365.com
#date:2018/5/15 14:19

import  requests
import os
from datetime import *

#创建文件夹
if os.path.exists('D:/抖音') == False:
    os.path.join('D:/', "抖音")
    os.mkdir('D:/抖音')
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, likeGecko)Chrome/66.0.3359.117 Safari/537.36'
    }

def get_video():
    #推荐视频入口
    url='https://cj.huitaodang.com/api/douyin/recommend/'
    req=requests.get(url,headers=headers).json()
    #获得json里面的列表
    info=(req['aweme_list'])
    #对列表进行循环
    for data in info:
        title=data['desc']
        nickname=data["nickname"]
        print(title,nickname)
        videolist=data['video']['play_addr']['url_list']
        for video in videolist:
            print(video)
            download_video(nickname,title,video)

def download_video(nickname,title,video):

    BASEDIR = os.path.join('D:/抖音/', title)
    # 捕获异常
    try:
        # 用requests去请求
        response = requests.get(video)
        # 写入文件
        with open(BASEDIR +nickname+ title + ".mp4", 'wb')as f:
            f.write(response.content)
    except Exception as  e:
        return None
if __name__=="__main__":
    i=0
    for i in  range(1000):
        get_video()
        bjtime = str(datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8)))).split('.')[0]
        print('北京时间: ' + bjtime)
        i+=1




