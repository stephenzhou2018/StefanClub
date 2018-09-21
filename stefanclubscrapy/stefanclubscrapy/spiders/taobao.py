# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
import json, time
from items import TaobaoProducts
from function import parse_taobao_products


class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['www.taobao.com']
    start_urls = ['http://www.taobao.com/']
    keywords = ['QUESTION']

    def start_requests(self):
        for keyword in self.keywords:
            browser = webdriver.Chrome()
            browser.get('https://www.taobao.com/')
            browser.find_element_by_class_name("search-combobox-input").send_keys(keyword)
            browser.find_element_by_class_name("btn-search").click()
            time.sleep(5)
            page_source = browser.page_source
            browser.close()
            g_page_config = page_source[page_source.index('g_page_config = {') + 15:page_source.index('g_srp_loadCss()')].strip()
            g_page_config_json = json.loads(g_page_config[:-1])
            mods = g_page_config_json["mods"]
            itemlist = mods["itemlist"]
            data = itemlist["data"]
            auctions = data["auctions"]
            for auction in auctions:
                taobaoproduct = parse_taobao_products(auction,keyword)
                yield taobaoproduct

