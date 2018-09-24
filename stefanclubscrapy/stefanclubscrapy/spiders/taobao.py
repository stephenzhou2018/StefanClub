# -*- coding: utf-8 -*-
import scrapy,requests
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
    last_twelve_url = 'https://s.taobao.com/api?_ksTS=1537784279315_208&callback=jsonp209&ajax=true&m=customized&stats_click=search_radio_all:1&q={keyword}&s=36&imgfile=&initiative_id=staobaoz_20180924&bcoffset=0&js=1&ie=utf8&rn=91a38a1dc028b177e8b2f5d17a1f1e05'

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
            last_twelve_response = requests.get(self.last_twelve_url.format(keyword=keyword))
            while last_twelve_response.text == '':
                last_twelve_response = requests.get(self.last_twelve_url.format(keyword=keyword))
            self.parse_last_twelve(last_twelve_response.text,keyword)

    def parse_last_twelve(self,response,keyword):
        dict_response = response[11:]
        dict_response = dict_response[:-2]
        json_response = json.loads(dict_response)
        customizedapi = json_response['API.CustomizedApi']
        itemlist = customizedapi['itemlist']
        auctions = itemlist['auctions']
        for auction in auctions:
            taobaoproduct = parse_taobao_products(auction, keyword, self.curr_num_of_img)
            self.curr_num_of_img = self.curr_num_of_img + 1
            yield taobaoproduct


