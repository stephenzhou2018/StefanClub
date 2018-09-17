# -*- coding: utf-8 -*-
import scrapy,os,urllib
from items import ZhihuHot
from bs4 import BeautifulSoup
from scrapy import Request,Selector
from selenium import webdriver
from pipelines import get_max_num
from function import get_zhihu_hotid
#from pyvirtualdisplay import Display


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com']

    headers = {
        'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",

    }
    max_userimg_num = get_max_num('zhihuhotuser')
    if max_userimg_num is None:
        max_userimg_num = 0
    curr_num_of_usim = max_userimg_num + 1

    max_newsimg_num = get_max_num('zhihuhotnews')
    if max_newsimg_num is None:
        max_newsimg_num = 0
    curr_num_of_neim = max_newsimg_num + 1

    def start_requests(self):
        #display = Display(visible=0, size=(800, 600))
        #display.start()

        browser = webdriver.Chrome()

        browser.get("https://www.zhihu.com/signin")
        browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys("13818248346")
        browser.find_element_by_css_selector(".SignFlow-password input").send_keys("kaihua1010")
        browser.find_element_by_css_selector(".Button.SignFlow-submitButton").click()
        import time
        time.sleep(10)
        Cookies = browser.get_cookies()
        cookie_dict = {}
        for cookie in Cookies:
            cookie_dict[cookie['name']] = cookie['value']
        browser.close()

        #display.stop()

        '''
        cookie_dict = {}
        cookie_dict['_xsrf'] = 'YapfGwAZLMF0xG66MGRahebpwTWssiMp'
        cookie_dict['_zap'] = 'aaeb426e-e3fe-4adc-a730-f21e54958363'
        cookie_dict['d_c0'] = 'AMDl7N8ONw6PTqRBOgSe3VBcN1Sgso03uoY=|1536993055'
        cookie_dict['capsion_ticket'] = '2|1:0|10:1537072100|14:capsion_ticket|44:ODkzNmNmNTExN2QwNDYzMmE2ZGQzZWMxNTFkNGIxYmE=|4477a216ce7dfa2047cc7641d4a63a577ec3b63a26faec26f8d315995881dad1'
        cookie_dict['z_c0'] = '2|1:0|10:1537072102|4:z_c0|92:Mi4xV2ZvX0F3QUFBQUFBd09YczN3NDNEaVlBQUFCZ0FsVk41aW1MWEFCSWYteU8zVW9wSHlvdHlsN1RFT3hNb0Y0aVpn|c3865b669f7767a0cb7f7360dee384375aef29fba98d7cd3e8592e72790826b4'
        cookie_dict['q_c1'] = '68adb565ac5f49b78fe08440a8927c2d|1536993067000|1536993067000'
        cookie_dict['tgw_l7_route'] = '56f3b730f2eb8b75242a8095a22206f8'
       '''
        yield Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict, callback=self.parse_main)

    def parse_main(self, response):
        zhihuhot = ZhihuHot()
        soup = BeautifulSoup(response.text, 'lxml')
        post_nodes = soup.select("div[class='Card TopstoryItem']")
        for post_node in post_nodes:
            sel = Selector(text=str(post_node), type="html", )
            feedsourceurl = sel.xpath('//a[@class="TopicLink"]//@href').extract()[0].strip()
            feedsourcetags = sel.xpath('//div[@aria-haspopup="true"]/text()')
            if len(feedsourcetags) > 0:
                feedsourcetag = sel.xpath('//div[@aria-haspopup="true"]/text()').extract()[0].strip()
            else:
                feedsourcetag =  None
            userimgsrcurl = sel.xpath('//img[@class="Avatar AuthorInfo-avatar"]//@src').extract()[0].strip()
            userimgurls = sel.xpath('//a[@class="UserLink-link"]//@href')
            if len(userimgurls) > 0:
                userimgurl = sel.xpath('//a[@class="UserLink-link"]//@href').extract()[0].strip()
            else:
                userimgurl = None
            usernames1 = sel.xpath('//a[@class="UserLink-link"]/text()')
            usernames2 = sel.xpath('//span[@class="UserLink AuthorInfo-name"]/text()')
            if len(usernames1) > 0:
                username = sel.xpath('//a[@class="UserLink-link"]/text()').extract()[0].strip()
            elif len(usernames2) > 0:
                username = sel.xpath('//span[@class="UserLink AuthorInfo-name"]/text()').extract()[0].strip()
            else:
                username = None
            userinfolist = sel.xpath('//div[@class="AuthorInfo-detail"]/div/div/text()')
            if len(userinfolist) > 0:
                userinfo = sel.xpath('//div[@class="AuthorInfo-detail"]/div/div/text()').extract()[0].strip()
            else:
                userinfo = None

            newsimg = sel.xpath('//div[@class="RichContent-cover-inner"]/img//@src')
            newsimg2 = sel.xpath('//div[@class="RichContent-cover-inner"]/div//@data-src')
            if len(newsimg) > 0:
                newsimgsrcurl = sel.xpath('//div[@class="RichContent-cover-inner"]/img//@src').extract()[0].strip()
            elif len(newsimg2) > 0:
                newsimgsrcurl = sel.xpath('//div[@class="RichContent-cover-inner"]/div//@data-src').extract()[0].strip()
            else:
                newsimgsrcurl = None
            if newsimgsrcurl is None:
                zhihuhot["newsimgsrcurl"] = None
                zhihuhot["newsimgnumber"] = None
            else:
                file_name1 = "zhihuhotnews_%s.jpg" % self.curr_num_of_neim
                file_path1 = os.path.join("D:\StefanClub\StefanClub\www\static\img\zhihu", file_name1)
                urllib.request.urlretrieve(newsimgsrcurl, file_path1)
                zhihuhot["newsimgsrcurl"] = "../static/img/zhihu/%s" % file_name1
                zhihuhot["newsimgnumber"] = self.curr_num_of_neim
                self.curr_num_of_neim = self.curr_num_of_neim + 1

            hasvideo = sel.xpath('//div[@class="RichContent-cover-play"]')
            if len(hasvideo) > 0:
                isvideo = 'TRUE'
            else:
                isvideo = 'FALSE'
            title1 = sel.xpath('//h2[@class="ContentItem-title"]/div/a')
            title2 = sel.xpath('//h2[@class="ContentItem-title"]/a')
            if len(title1) > 0:
                title = sel.xpath('//h2[@class="ContentItem-title"]/div/a/text()').extract()[0].strip()
                titleurl = sel.xpath('//h2[@class="ContentItem-title"]/div/a//@href').extract()[0].strip()
            elif len(title2) > 0:
                title = sel.xpath('//h2[@class="ContentItem-title"]/a/text()').extract()[0].strip()
                titleurl = sel.xpath('//h2[@class="ContentItem-title"]/a//@href').extract()[0].strip()
            else:
                title = 'Empty title,It will be dropped by redis control except the first one'
                titleurl = None
            if titleurl is not None:
                if titleurl[1:9] == 'question':
                    titleurl = '//www.zhihu.com' + titleurl
            hotid = get_zhihu_hotid(titleurl)
            newscontent = sel.xpath('//span[@class="RichText ztext CopyrightRichText-richText"]/text()').extract()[0].strip()
            infavorqty1 = sel.xpath('//button[@class="Button VoteButton VoteButton--up"]/text()').extract()[0].strip()
            infavorqty2 = sel.xpath('//button[@class="Button VoteButton VoteButton--up"]/text()').extract()[1].strip()
            infavorqty = infavorqty1 + infavorqty2
            infavorqty_list = list(infavorqty)
            infavorqty_list.insert(2, " ")
            infavorqty = "".join(infavorqty_list)
            comment_title = sel.xpath('//button[@class="Button ContentItem-action Button--plain Button--withIcon Button--withLabel"]/text()').extract()[0].strip()
            file_name = "zhihuhotuser_%s.jpg" % self.curr_num_of_usim
            file_path = os.path.join("D:\StefanClub\StefanClub\www\static\img\zhihu", file_name)
            urllib.request.urlretrieve(userimgsrcurl, file_path)
            zhihuhot["userimgsrcurl"] = "../static/img/zhihu/%s" % file_name
            zhihuhot["userimgnumber"] = self.curr_num_of_usim
            self.curr_num_of_usim = self.curr_num_of_usim + 1

            zhihuhot["feedsourcetag"] = feedsourcetag
            zhihuhot["feedsourceurl"] = feedsourceurl
            zhihuhot["userimgurl"] = userimgurl
            zhihuhot["username"] = username
            zhihuhot["userinfo"] = userinfo
            zhihuhot["newsimgurl"] = None
            zhihuhot["isvideo"] = isvideo
            zhihuhot["title"] = title
            zhihuhot["titleurl"] = titleurl
            zhihuhot["hotid"] = hotid
            zhihuhot["newscontent"] = newscontent
            zhihuhot["infavorqty"] = infavorqty
            zhihuhot["comment_url"] = None
            zhihuhot["comment_title"] = comment_title
            zhihuhot["share_url"] = None

            yield zhihuhot
