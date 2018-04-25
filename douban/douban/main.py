#!usr/bin/env python
# -*- coding: utf-8 -*-
#_Author:shenshi
#date:2018/4/25 21:59
from  scrapy.cmdline import  execute
import sys
import os
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
# execute(['scrapy','crawl','lao4g'])
execute(['scrapy','crawl','douban250'])