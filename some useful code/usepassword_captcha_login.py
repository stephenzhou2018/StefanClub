# -*- coding: utf-8 -*-
import scrapy,re,demjson
from items import ZhihuHot
from bs4 import BeautifulSoup
from scrapy import Request,Selector,FormRequest


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com']

    headers = {
        'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",

    }

    def start_requests(self):
        #return [scrapy.Request('https://www.zhihu.com/#signin',headers=self.headers,callback=self.login)]
        return [Request('http://www.zhihu.com/explore', callback=self.login)]

    def login(self,response):
        response_text = response.text
        match_obj = re.match('.*name="_xsrf" value="(.*?)"', response_text, re.DOTALL)
        xsrf=''
        if match_obj:
            xsrf = match_obj.group(1)
        if xsrf:
            post_data = {
                "_xsrf": xsrf,
                "phone_num": "13818248346",
                "password": "kaihua1010",
                'captcha': '',
            }
            import time
            t = str(int(time.time() * 1000))
            captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
            yield Request(captcha_url, meta={"post_data":post_data}, callback=self.login_after_captcha)

    def login_after_captcha(self, response):
        with open("zhihucaptcha.jpg",'wb') as f:
            f.write(response.body)
        try:
            from PIL import Image
            im = Image.open("zhihucaptcha.jpg")
            im.show()
        except:
            pass
        captcha = input("请输入验证码>:").strip()
        post_data = response.meta.get("post_data")
        post_data["captcha"] = captcha
        post_url = "https://www.zhihu.com/login/phone_num"
        yield FormRequest(
            url=post_url,
            formdata=post_data,
            headers=self.headers,
            callback=self.parse_main,
        )

    def after_login(self,response):
        '''
        验证服务器的返回数据判断是否成功,我们使用scrapy会自动携带我们登录后的cookie
        yield  是为了保持会话，使用cookie继续访问其他页面
        :param response:
        :return:
        '''
        text_json = demjson.encode(response.text)
        print(text_json)
        for url in self.start_urls:
            #yield self.make_requests_from_url(url,dont_filter=True,header=self.headers)
            yield Request(url, dont_filter=True, callback=self.parse_main)

    def parse_main(self, response):
        zhihuhot = ZhihuHot()
        soup = BeautifulSoup(response.text, 'lxml')
        post_nodes = soup.select("div[class='Card TopstoryItem']")
        for post_node in post_nodes:
            sel = Selector(text=str(post_node), type="html", )
            feedsourceurl = sel.xpath('//a[@class="TopicLink"]/@href').extract()[0].strip()
            feedsourcetag = sel.xpath('//div[@id="Popover3-toggle"]/text()').extract()[0].strip()

