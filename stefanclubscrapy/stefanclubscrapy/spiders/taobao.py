# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
import json, time
from items import TaobaoProducts
from function import parse_taobao_products
from pipelines import get_max_num

class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['www.taobao.com']
    start_urls = ['http://www.taobao.com/']
    keywords = ['QUESTION']

    max_img_num = get_max_num('taobaoproduct')
    if max_img_num is None:
        max_img_num = 0
    curr_num_of_img = max_img_num + 1

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
                taobaoproduct = parse_taobao_products(auction,keyword,self.curr_num_of_img)
                self.curr_num_of_img = self.curr_num_of_img + 1
                yield taobaoproduct

