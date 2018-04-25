# -*- coding: utf-8 -*-
import scrapy
import  time
from douban.items import DoubanItem
from urllib import parse
from scrapy.http import Request
class Douban250Spider(scrapy.Spider):
    name = 'douban250'
    allowed_domains = ['movie.douban.com/top250']
    # start_urls = ['https://movie.douban.com/top250']
    headers = {
        'Cookie': 'll = "108258";bid = Ld - Cxx6zAZ8',
        'Host': 'movie.douban.com',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    def start_requests(self):

        url = 'https://movie.douban.com/top250'
        yield Request(url, headers=self.headers)

    def parse(self, response):
        item=DoubanItem
        movie_intro = response.xpath('//ol[@class="grid_view"]/li')
        for movie in movie_intro:
            item = {}
            # 电影名称
            name = movie.xpath('.//div[@class="hd"]/a/span[1]/text()').extract_first()
            #评分人数
            score_num=movie.xpath('.//div/span[4]/text()').extract_first()
            #评分
            rank = movie.xpath('.//span[@class="rating_num"]/text()').extract_first()
            item = {
                'name': name,
                'rank': rank,
                'score_num':score_num,
            }
            # 进入电影详情页面的url
            detail_url = movie.xpath('.//a/@href').extract_first()
            # 获取详细信息
            yield scrapy.Request(url=detail_url, callback=self.parse_info, meta={'item': item}, dont_filter=True)

            # 翻页
        next_url = response.xpath('//span[@class="next"]/a/@href').extract()
        if next_url:
            next_url = 'https://movie.douban.com/top250' + next_url[0]
            yield Request(next_url, headers=self.headers,callback=self.parse,dont_filter=True)

    # 解析每一条电影链接对应的详情页信息
    def parse_info(self, response):
        item = response.meta['item']
        #获取imdb链接
        item['imdb']=response.xpath('//div[@class="article"]//div[@id="info"]/a[1]/@href').extract_first()
        #获取简介
        item['introduce']=response.xpath('//*[@id="link-report"]/span[1]/span/text()').extract_first("")
        #获取封面图片
        item['img']=response.xpath('//div[@class="article"]//div[@id="mainpic"]//img/@src').extract_first()
        time.sleep(1)
        yield item
