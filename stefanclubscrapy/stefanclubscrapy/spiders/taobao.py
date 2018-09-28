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
    keywords = ['UNIQLO', 'SUPERME', 'NIKE', 'ADIDAS', 'APPLE', 'HUAWEI']
    #keywords = ['UNIQLO', 'SUPERME', 'NIKE', 'ADIDAS']
    last_twelve_url = 'https://s.taobao.com/api?_ksTS=1537784279315_208&callback=jsonp209&ajax=true&m=customized&stats_click=search_radio_all:1&q={keyword}&s=36&imgfile=&initiative_id=staobaoz_20180924&bcoffset=0&js=1&ie=utf8&rn=91a38a1dc028b177e8b2f5d17a1f1e05'
    next_page_url = 'https://s.taobao.com/search?data-key=s&data-value={datavalue}&ajax=true&_ksTS=1537791664734_887&callback=jsonp888&q={keyword}&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20180920&ie=utf8&bcoffset=4&p4ppushleft=1%2C48'

    max_img_num = get_max_num('taobaoproduct')
    if max_img_num is None:
        max_img_num = 0
    curr_num_of_img = max_img_num + 1

    def start_requests(self):
        yield scrapy.Request('http://www.taobao.com/', callback=self.parse)

    def parse(self,response):
        for keyword in self.keywords:
            browser = webdriver.Chrome()
            browser.get('https://www.taobao.com/')
            browser.find_element_by_class_name("search-combobox-input").send_keys(keyword)
            browser.find_element_by_class_name("btn-search").click()
            time.sleep(5)
            while browser.page_source.find('g_page_config') == -1:
                browser.refresh()
            page_source = browser.page_source
            browser.close()
            #yield self.parse_first_batch(page_source,keyword)
            g_page_config = page_source[page_source.index('g_page_config = {') + 15:page_source.index('g_srp_loadCss()')].strip()
            g_page_config_json = json.loads(g_page_config[:-1])
            modsfirst = g_page_config_json["mods"]
            itemlist_first = modsfirst["itemlist"]
            data_first = itemlist_first["data"]
            auctions_first = data_first["auctions"]
            for auction_first in auctions_first:
                taobaoproduct = parse_taobao_products(auction_first, keyword, self.curr_num_of_img)
                self.curr_num_of_img = self.curr_num_of_img + 1
                yield taobaoproduct

            last_twelve_response = requests.get(self.last_twelve_url.format(keyword=keyword))
            while last_twelve_response.text == '':
                last_twelve_response = requests.get(self.last_twelve_url.format(keyword=keyword))
            #yield self.parse_last_twelve(last_twelve_response.text,keyword)
            dict_response_last = last_twelve_response.text[11:]
            dict_response_last = dict_response_last[:-2]
            json_response_last = json.loads(dict_response_last)
            customizedapi = json_response_last['API.CustomizedApi']
            itemlist_last = customizedapi['itemlist']
            auctions_last = itemlist_last['auctions']
            for auction_last in auctions_last:
                taobaoproduct = parse_taobao_products(auction_last, keyword, self.curr_num_of_img)
                self.curr_num_of_img = self.curr_num_of_img + 1
                yield taobaoproduct

            # get next page by click the nextlink
            # browser.find_elements_by_partial_link_text('下一页')[0].click()
            # next_page_source = browser.page_source
            for i in range(30):
                nextpage_response = requests.get(self.next_page_url.format(datavalue=44 * (i+1), keyword=keyword))
                while nextpage_response.text == '':
                    nextpage_response = requests.get(self.next_page_url.format(datavalue=44 * (i+1), keyword=keyword))
                #yield self.parse_next_page(nextpage_response.text,keyword)
                dict_response_next = nextpage_response.text[11:]
                dict_response_next = dict_response_next[:-2]
                json_response_next = json.loads(dict_response_next)
                modsnext = json_response_next['mods']
                itemlist_next = modsnext['itemlist']
                data_next = itemlist_next['data']
                auctions_next = data_next['auctions']
                for auction_next in auctions_next:
                    taobaoproduct = parse_taobao_products(auction_next, keyword, self.curr_num_of_img)
                    self.curr_num_of_img = self.curr_num_of_img + 1
                    yield taobaoproduct

    def parse_first_batch(self,page_source,keyword):
        g_page_config = page_source[
                        page_source.index('g_page_config = {') + 15:page_source.index('g_srp_loadCss()')].strip()
        g_page_config_json = json.loads(g_page_config[:-1])
        mods = g_page_config_json["mods"]
        itemlist = mods["itemlist"]
        data = itemlist["data"]
        auctions = data["auctions"]
        for auction in auctions:
            taobaoproduct = parse_taobao_products(auction, keyword, self.curr_num_of_img)
            self.curr_num_of_img = self.curr_num_of_img + 1
            yield taobaoproduct

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

    def parse_next_page(self,response,keyword):
        dict_response = response[11:]
        dict_response = dict_response[:-2]
        json_response = json.loads(dict_response)
        mods = json_response['mods']
        itemlist = mods['itemlist']
        data = itemlist['data']
        auctions = data['auctions']
        for auction in auctions:
            taobaoproduct = parse_taobao_products(auction, keyword, self.curr_num_of_img)
            self.curr_num_of_img = self.curr_num_of_img + 1
            yield taobaoproduct


