# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 电影名称
    name = scrapy.Field()
    # 封面图片
    img = scrapy.Field()
    # 评分
    rank = scrapy.Field()
    # 评论人数
    score_num = scrapy.Field()
    # 简介
    introduce=scrapy.Field()
    # IMDB链接
    imdb=scrapy.Field()





