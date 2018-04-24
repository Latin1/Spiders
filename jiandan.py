#!usr/bin/env python
# -*- coding: utf-8 -*-
#_Author:shenshi
#date:2018/4/23 21:33
import requests
from bs4 import BeautifulSoup
import base64
import hashlib
import re
#这里必须加headers，不然会显示403错误
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}

def _md5(value):
    '''md5加密'''
    m = hashlib.md5()
    m.update(value.encode('utf8'))
    return m.hexdigest()

def _base64_decode(data):
    '''bash64解码，要注意原字符串长度报错问题'''
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += '=' * missing_padding
    return base64.b64decode(data)


def get_imgurl(m, r='', d=0):
    '''解密获取图片链接'''
    e = "DECODE"
    q = 4
    r =_md5(r)
    o = _md5(r[0:0 + 16])
    n = _md5(r[16:16 + 16])
    l = m[0:q]
    c = o + _md5(o + l)
    m = m[q:]
    k = _base64_decode(m)
    h = list(range(256))
    b = [ord(c[g % len(c)]) for g in range(256)]

    f = 0
    for g in range(0, 256):
        f = (f + h[g] + b[g]) % 256
        tmp = h[g]
        h[g] = h[f]
        h[f] = tmp

    t = ""
    p, f = 0, 0
    for g in range(0, len(k)):
        p = (p + 1) % 256
        f = (f + h[p]) % 256
        tmp = h[p]
        h[p] = h[f]
        h[f] = tmp
        t += chr(k[g] ^ (h[(h[p] + h[f]) % 256]))
    t = t[26:]
    return t

def get_r(js_url):
    '''获取关键字符串'''
    js = requests.get(js_url).text
    _r = re.findall('jd[\w\d]+\(e,"(.*?)"\)', js)[-1]
    return _r

def get_urls(url):
    '''获取一个页面的所有图片的链接'''
    html = requests.get(url, headers=headers).text
    js_url = 'http:' + re.findall('<script src="(//cdn.jandan.net/static/min/[\w\d]+\.\d+\.js)"></script>', html)[-1]
    _r = get_r(js_url)
    soup = BeautifulSoup(html, 'lxml')
    tags = soup.select('.img-hash')
    for tag in tags:
        img_hash = tag.text
        img_url = get_imgurl(img_hash,_r,d=0)
        print(img_url)
def get_allurl():
    url = 'http://jandan.net/ooxx/'
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')
    # 获得最后一页的页码数
    page_all = soup.find('span', class_="current-comment-page").get_text()[1:-1]
    # print(page_all)
    urllist = []
    # 通过for循环得到所有的url,由于range取前不取后，因此需要加1，才能获得所有的url
    for page in range(1, int(page_all) + 1):
        allurl = url + 'page-' + str(page)
        yield allurl

    # 获得本页的所有图片
if __name__ == '__main__':
    get_allurl()
    for urllist in get_allurl():
       get_urls(urllist)










