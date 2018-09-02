# -*- coding: utf-8 -*-
import scrapy


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['https://www.zhihu.com/']
    start_urls = ['http://https://www.zhihu.com//']

    def parse(self, response):
        pass
