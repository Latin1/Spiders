# -*- coding: utf-8 -*-
#_Author:www.haofun365.com
#date:2018/5/14 0:58
import requests
from bs4 import  BeautifulSoup
from lxml import  *
import  re
import os
import  multiprocessing  as mp
s=requests.session()
headers={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}
#主页
baseurl='http://www.sstaotu.com/'
#每页的url
goUrl=['http://www.sstaotu.com/index.php?s=/Home/Index/index/p/{}.html'.format(id)for id in range(1,15)]
#创建文件夹
if os.path.exists('D:/shenshi') == False:
    os.path.join('D:/', "shenshi")
    os.mkdir('D:/shenshi')
#获取到每页的url
def geturl():
    for url in goUrl:
        req=s.get(url,headers=headers)
        if req.status_code==200:
            html=req.text
            parse_url(html)
        else:
            print('该页面不存在')
#获取每个图片集的url
def parse_url(html):
    soup=BeautifulSoup(html,'lxml')
    link=soup.find_all('div',class_='postlist')
    soup2=BeautifulSoup(str(link),'lxml')
    AllUrl=soup2.select('span a')
    for each in AllUrl:
        direct_url=each.get('href')
        #从这里获得图片详情页地址的数字
        Allnum=int(re.findall('\d{2,3}',direct_url)[0])
        get_img(Allnum,direct_url)
#获取图片
def get_img(number,urls):
    urls = ['http://www.sstaotu.com/index.php?s=/Home/Article/detail/id/{}/p/{}.html' .format(number,page)for page in range(1,50)]
    # print(urls)
    for url in urls:
        response=s.get(url,headers=headers)
        if response.status_code==200:
            image_url=response.content
            soup=BeautifulSoup(image_url,'lxml')
            img=soup.find_all('div',class_='main-image')
            soup2 = BeautifulSoup(str(img), 'lxml')
            pics = soup2.select('img')
            #图片的标题
            title = soup.select('h2')[0].get_text()
            print(title)
            for pic in pics:
                #每页的图片链接
                piclist =pic.get('src')
                print(piclist)
                #正则匹配图片的最后两位数字
                imgnum=re.findall('http://img.xichele.cn:8088/FileUpload/tu/.*(\d\d).jpg',piclist)[0]
                BASEDIR=os.path.join('D:/shenshi/',title)
                #捕获异常
                try:
                    #用requests去请求图片的url
                    down_url=s.get(piclist)
                    #写入文件
                    with open(BASEDIR+str(imgnum)+ ".jpg", 'wb')as f:
                        f.write(down_url.content)
                except Exception as  e:
                    return  None
        else:
            print('此网页没有图片')

if __name__ =="__main__":
    geturl()



