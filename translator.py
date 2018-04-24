#!usr/bin/env python
# -*- coding: utf-8 -*-
#_Author:wudi666
#date:2018/4/22 16:29

from urllib import request
from urllib import parse
import json

if __name__ == "__main__":
    #对应上图的Request URL
    Request_URL = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
    #创建Form_Data字典，存储上图的Form Data
    Form_Data = {}
    Form_Data['i'] = input('输入需要翻译的单词：')
    Form_Data['from']='AUTO'
    Form_Data['to'] = 'AUTO'
    Form_Data['smartresult'] = 'dict'
    Form_Data['client'] = 'fanyideskweb'
    Form_Data['doctype'] = 'json'
    Form_Data['version'] = '2.1'
    Form_Data['keyfrom'] = 'fanyi.web'
    Form_Data['action'] = 'Y_BY_REALTIME'
    Form_Data['typoResult']='false'
    #使用urlencode方法转换标准格式
    data = parse.urlencode(Form_Data).encode('utf-8')
    #传递Request对象和转换完格式的数据
    response = request.urlopen(Request_URL,data)
    #读取信息并解码
    html = response.read().decode('utf-8')
    #使用JSON
    translateResult = json.loads(html)
    #找到翻译结果
    translate_results = translateResult['translateResult'][0][0]['tgt']
    #输出翻译结果
    print("翻译的结果是：%s" % translate_results)