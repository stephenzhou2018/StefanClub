# -*- coding: utf-8 -*-
import scrapy, os, urllib, json, datetime, time, requests
from items import ZhihuHot,ZhihuHotComment,ZhihuHotContent
from bs4 import BeautifulSoup
from scrapy import Request,Selector
from selenium import webdriver
from pipelines import get_max_num
from function import get_zhihu_hotid,get_comment_qty
#from pyvirtualdisplay import Display


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com']

    zhuanlan_comment_url = 'https://www.zhihu.com/api/v4/articles/{hotid}/comments?include=data%5B*%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author%2Calgorithm_right&order=normal&limit=20&offset={offset}&status=open'
    answer_comment_url = 'https://www.zhihu.com/api/v4/answers/{hotid}/comments?include=data%5B*%5D.author%2Ccollapsed%2Creply_to_author%2Cdisliked%2Ccontent%2Cvoting%2Cvote_count%2Cis_parent_author%2Cis_author%2Calgorithm_right&order=normal&limit=20&offset={offset}&status=open'
    # headers = {'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",}
    headers = {}
    max_userimg_num = get_max_num('zhihuhotuser')
    if max_userimg_num is None:
        max_userimg_num = 0
    curr_num_of_usim = max_userimg_num + 1

    max_newsimg_num = get_max_num('zhihuhotnews')
    if max_newsimg_num is None:
        max_newsimg_num = 0
    curr_num_of_neim = max_newsimg_num + 1

    max_comuserimg_num = get_max_num('zhihuhotcomments')
    if max_comuserimg_num is None:
        max_comuserimg_num = 0
    curr_num_of_comuser = max_comuserimg_num + 1

    def start_requests(self):
        #display = Display(visible=0, size=(800, 600))
        #display.start()
        s = requests.Session()
        s.headers.clear()
        browser = webdriver.Chrome()
        '''browser2 = webdriver.Firefox()
        browser2.get("https://www.zhihu.com/signin")
        browser2.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys("13818248346")
        browser2.find_element_by_css_selector(".SignFlow-password input").send_keys("kaihua1010")
        browser2.find_element_by_css_selector(".Button.SignFlow-submitButton").click()
        time.sleep(5)
        Cookies2 = browser2.get_cookies()'''

        browser.get("https://www.zhihu.com/signin")
        browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys("13818248346")
        browser.find_element_by_css_selector(".SignFlow-password input").send_keys("kaihua1010")
        browser.find_element_by_css_selector(".Button.SignFlow-submitButton").click()
        time.sleep(10)
        Cookies = browser.get_cookies()
        cookie_dict = {}
        '''cookie = [item["name"] + "=" + item["value"] for item in Cookies]
        cookiestr = '; '.join(item for item in cookie)
        self.headers['cookie'] = cookiestr'''
        for cookie in Cookies:
            cookie_dict[cookie['name']] = cookie['value']
            s.cookies.set(cookie['name'], cookie['value'])

        browser.close()
        html2 = s.get('https://www.zhihu.com/question/263892920/answer/405697336').text
        print(html2)
        html3 = s.get(self.start_urls[0]).text
        print(html3)
        self.headers = s.headers
        #display.stop()

        '''cookie_dict = {}
        cookie_dict['_xsrf'] = 'a1807a2e-e8da-4464-bcc0-b11be259f42b'
        cookie_dict['_zap'] = '1e5ccdb9-7860-466f-9a59-ff9cb19e072d'
        cookie_dict['d_c0'] = 'ALAnFykIXg6PTtXBbHxOihH1-UmQKy8guOQ=|1539608541'
        cookie_dict['capsion_ticket'] = '2|1:0|10:1539790364|14:capsion_ticket|44:NWIxZTRlYjUxOTg3NGI5MjgwODBhZjYwNmEwNTFhYTI=|4c1810d7fdf17461da2dc94a82756002cab3899386af9fef230ec3efd8f410f9'
        cookie_dict['z_c0'] = '2|1:0|10:1539790372|4:z_c0|92:Mi4xV2ZvX0F3QUFBQUFBc0NjWEtRaGVEaVlBQUFCZ0FsVk5KS1MwWEFEXy0wZTFkX1I3SjhwTlRTSnUxSDRQajhfcHdR|a100b4ed646d6454be56a0be8f3257fddb1ead83eabe52056221759123a6d005'
        cookie_dict['q_c1'] = '1d154dfb0c3c49b5afcdf6c78fc70148|1539608544000|1539608544000'
        cookie_dict['tgw_l7_route'] = '170010e948f1b2a2d4c7f3737c85e98c'
        cookie_dict['__utma'] = '51854390.302433648.1539609652.1539609652.1539609652.1'
        cookie_dict['__utmc'] = '51854390'
        cookie_dict['__utmz'] = '51854390.1539609652.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/hot'
        cookie_dict['__utmv'] = '51854390.100--|2=registration_date=20160715=1^3=entry_date=20160715=1'
        cookie_dict['tst'] = 'r'
        cookie_dict['__gads'] = 'ID=fa1c97a341ad2943:T=1539696957:S=ALNI_MZJ7ws-b5ObURSAQlBAGi8pbTmD6g'
'''
        yield Request(url=self.start_urls[0], dont_filter=True, meta={"cookies": cookie_dict}, cookies=cookie_dict, callback=self.parse_main,)
        #yield Request(url=self.start_urls[0], dont_filter=True, meta={"cookies": cookie_dict}, cookies=cookie_dict,callback=self.parse_main, )
        #yield Request(url=self.start_urls[0], dont_filter=True, headers=self.headers, callback=self.parse_main)

    def parse_main(self, response):
        zhihuhot = ZhihuHot()
        cookie_dict = response.meta.get("cookies", "")
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
            hottype = None
            if titleurl is not None:
                if titleurl[1:9] == 'question':
                    titleurl = '//www.zhihu.com' + titleurl
                    hottype = 'question'
                if titleurl[2:10] == 'zhuanlan':
                    hottype = 'zhuanlan'
            hotid = None
            if titleurl is not None:
                hotid = get_zhihu_hotid(titleurl)
            newscontent = sel.xpath('//span[@class="RichText ztext CopyrightRichText-richText"]/text()').extract()[0].strip()
            infavorqty1 = sel.xpath('//button[@class="Button VoteButton VoteButton--up"]/text()').extract()[0].strip()
            infavorqty2 = sel.xpath('//button[@class="Button VoteButton VoteButton--up"]/text()').extract()[1].strip()
            infavorqty = infavorqty1 + infavorqty2
            infavorqty_list = list(infavorqty)
            infavorqty_list.insert(2, " ")
            infavorqty = "".join(infavorqty_list)
            comment_title = sel.xpath('//button[@class="Button ContentItem-action Button--plain Button--withIcon Button--withLabel"]/text()').extract()[0].strip()
            comment_qty = get_comment_qty(comment_title)
            comment_page = comment_qty // 20 + (1 if comment_qty % 20 > 0 else 0)
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

            if hotid is not None:
                yield zhihuhot
                if hottype == 'question':
                    for i in range(comment_page):
                        yield Request(url=self.answer_comment_url.format(hotid=hotid, offset=i * 20), meta={"hotid": hotid}, cookies=cookie_dict, callback=self.parse_zhihuhot_comment)
                elif hottype == 'zhuanlan':
                    for i in range(comment_page):
                        yield Request(url=self.zhuanlan_comment_url.format(hotid=hotid, offset=i * 20), meta={"hotid": hotid}, cookies=cookie_dict, callback=self.parse_zhihuhot_comment)
                yield Request(url=titleurl, meta={"hotid": hotid, "hottype": hottype}, cookies=cookie_dict, callback=self.parse_zhihuhot_content)

    def parse_zhihuhot_comment(self,response):
        hotid = response.meta.get("hotid", "")
        resultjson = json.loads(response.body)
        comments = resultjson['data']
        comment_item  = ZhihuHotComment()
        for comment in comments:
            commentid = comment['id']
            author = comment['author']
            author_member = author['member']
            userimgsrcurl = author_member['avatar_url']
            url_token = author_member['url_token']
            userimgurl = '//www.zhihu.com/people/' + url_token
            username = author_member['name']
            replytime = comment['created_time']
            replytime = datetime.datetime.fromtimestamp(replytime)
            content = comment['content']
            infavorqty = comment['vote_count']
            replytouser = None
            replytouserurl = None
            if "reply_to_author" in comment.keys():
                reply_to_author = comment['reply_to_author']
                if reply_to_author is not None:
                    reply_to_author_member = reply_to_author['member']
                    replytouser = reply_to_author_member['name']
                    replytouser_urltoken = reply_to_author_member['url_token']
                    replytouserurl = '//www.zhihu.com/people/' + replytouser_urltoken
            file_name = "zhihuhotcomuser_%s.jpg" % self.curr_num_of_comuser
            file_path = os.path.join("D:\StefanClub\StefanClub\www\static\img\zhihu", file_name)
            urllib.request.urlretrieve(userimgsrcurl, file_path)
            comment_item["userimgsrcurl"] = "../static/img/zhihu/%s" % file_name
            comment_item["userimgnumber"] = self.curr_num_of_comuser
            self.curr_num_of_comuser = self.curr_num_of_comuser + 1

            comment_item["commentid"] = commentid
            comment_item["hotid"] = hotid
            comment_item["userimgurl"] = userimgurl
            comment_item["username"] = username
            comment_item["replytouser"] = replytouser
            comment_item["replytouserurl"] = replytouserurl
            comment_item["replytime"] = replytime
            comment_item["content"] = content
            comment_item["infavorqty"] = infavorqty

            yield comment_item


    def parse_zhihuhot_content(self,response):
        hotid = response.meta.get("hotid", "")
        partno = 1
        hottype = response.meta.get("hottype", "")
        zhihuhot_content = ZhihuHotContent()
        soup = BeautifulSoup(response.text, 'lxml')
        if hottype == 'question':
            post_node = soup.select("span[class='CopyrightRichText-richText']")
        else:
            post_node = soup.select("div[class='Post-RichText']")
        sel = Selector(text=str(post_node), type="html", )
        test = sel.xpath('*')


