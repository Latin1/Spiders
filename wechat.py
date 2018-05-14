#!usr/bin/env python
# -*- coding: utf-8 -*-
#_Author:shenshi
#date:2018/4/25 10:16
# -*- coding:utf-8 -*-
import requests
import time
import os
import hashlib
import json
import re

LOGIN_COOKIES_DICT = {}


# def _password(pwd):
#     ha = hashlib.md5()
#     ha.update(pwd)
#     return ha.hexdigest()

uuid = ''
def login():
    login_dict = {
        'appid':'wx782c26e4c19acffb',
        'redirect_uri': 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage',
    'fun': 'new',
    'lang': 'zh_',
    '_': int(time.time())
}

    login_res = requests.get(
        url="https://login.wx.qq.com/jslogin",params=login_dict).text
    print(login_res)
    regx = r'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+?)"'
    pm = re.search(regx, login_res)
    code = pm.group(1)
    uuid = pm.group(2)
    print(code, uuid)
    show2DimensionCode(uuid)

    if code == '200':
        return True
    return False

def show2DimensionCode(uuid):

    url = 'https://login.weixin.qq.com/qrcode/' + uuid

    response=requests.get(url).content
    with open('wechat.jpg', 'wb')as f:
        f.write(response)# 以二进制（b）打开二维码图片
    print('请使用手机微信扫描二维码登录')
    time.sleep(1)  # 延时1秒
    # os.system('call %s' % 'wechat.jpg')  # 打开图片
def login_in():
    data = {
         'loginicon': 'true',
         'uuid': '4eebhSLlrg==',
         'tip': 0,
         'r': '79450238',
         '_': int(time.time())
     }
    login_url = 'https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login'
    req = requests.get(login_url, params=data)

    print(req.url)

login_in()
if __name__=="__main__":
    login()




    # # 登陆成功之后获取服务器响应的cookie
    # resp_cookies_dict = login_res.cookies.get_dict()
    # # 登陆成功后，获取服务器响应的内容
    # resp_text = login_res.text
    # # 登陆成功后，获取token
    # token = re.findall(".*token=(\d+)", resp_text)[0]
    #
    # return {'token': token, 'cookies': resp_cookies_dict}


# def standard_user_list(content):
#     content = re.sub('\s*', '', content)
#     content = re.sub('\n*', '', content)
#     data = re.findall("""cgiData=(.*);seajs""", content)[0]
#     data = data.strip()
#     while True:
#         temp = re.split('({)(\w+)(:)', data, 1)
#         if len(temp) == 5:
#             temp[2] = '"' + temp[2] + '"'
#             data = ''.join(temp)
#         else:
#             break
#
#     while True:
#         temp = re.split('(,)(\w+)(:)', data, 1)
#         if len(temp) == 5:
#             temp[2] = '"' + temp[2] + '"'
#             data = ''.join(temp)
#         else:
#             break
#
#     data = re.sub('\*\d+', "", data)
#     ret = json.loads(data)
#     return ret
#
#
# def get_user_list():
#     login_dict = login()
#     LOGIN_COOKIES_DICT.update(login_dict)
#
#     login_cookie_dict = login_dict['cookies']
#     res_user_list = requests.get(
#         url="https://mp.weixin.qq.com/cgi-bin/user_tag",
#         params={"action": "get_all_data", "lang": "zh_CN", "token": login_dict['token']},
#         cookies=login_cookie_dict,
#         headers={'Referer': 'https://mp.weixin.qq.com/cgi-bin/login?lang=zh_CN'}
#     )
#     user_info = standard_user_list(res_user_list.text)
#     for item in user_info['user_list']:
#         print
#         "%s %s " % (item['nick_name'], item['id'],)
#
#
# def send_msg(user_fake_id, content='啥也没发'):
#     login_dict = LOGIN_COOKIES_DICT
#
#     token = login_dict['token']
#     login_cookie_dict = login_dict['cookies']
#
#     send_dict = {
#         'token': token,
#         'lang': "zh_CN",
#         'f': 'json',
#         'ajax': 1,
#         'random': "0.5322618900912392",
#         'type': 1,
#         'content': content,
#         'tofakeid': user_fake_id,
#         'imgcode': ''
#     }
#
#     send_url = "https://mp.weixin.qq.com/cgi-bin/singlesend?t=ajax-response&f=json&token=%s&lang=zh_CN" % (token,)
#     message_list = requests.post(
#         url=send_url,
#         data=send_dict,
#         cookies=login_cookie_dict,
#         headers={'Referer': 'https://mp.weixin.qq.com/cgi-bin/login?lang=zh_CN'}
#     )
#
#
# get_user_list()
# fake_id = raw_input('请输入用户ID:')
# content = raw_input('请输入消息内容:')
# send_msg(fake_id, content)
#





