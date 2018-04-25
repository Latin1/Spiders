# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class DoubanPipeline(object):

    def open_spider(self, spider):
        self.f = open('movie.json', 'w', encoding='utf-8')

    # 退出就关闭文件
    def close_spider(self, spider):
        self.f.close()

    # 此处的item参数就是从douban250.py中的parse方法返回的
    # 每返回一个item，这里就调用一次
    def process_item(self, item, spider):
        print(item)
        string = json.dumps(item, ensure_ascii=False, indent=4)
        self.f.write(string + '\n')

        return item