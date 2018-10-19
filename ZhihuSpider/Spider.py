# -*- coding: utf-8 -*-
import os, urllib, json, datetime, time, requests
from items import ZhihuHot,ZhihuHotComment,ZhihuHotContent
from bs4 import BeautifulSoup
from scrapy import Selector
from selenium import webdriver
from pipelines import get_max_num
from function import get_zhihu_hotid,get_comment_qty
from ReplacePipline import DuplicatesRecord,RedisDeDuplicate,InsertToMysql,UpdateCollapseNo


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

s = requests.Session()
s.headers.clear()
duplicate_record = DuplicatesRecord()
redis_deduplicate = RedisDeDuplicate()
inserttomysql = InsertToMysql()
update_collapseno = UpdateCollapseNo()

def start_requests():
    browser = webdriver.Chrome()
    browser.get("https://www.zhihu.com/signin")
    browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys("13818248346")
    browser.find_element_by_css_selector(".SignFlow-password input").send_keys("kaihua1010")
    browser.find_element_by_css_selector(".Button.SignFlow-submitButton").click()
    time.sleep(10)
    Cookies = browser.get_cookies()
    for cookie in Cookies:
        s.cookies.set(cookie['name'], cookie['value'])
    browser.close()
    html = s.get(start_urls[0]).text
    parse_main(html)
    update_collapseno.updatedata()


def parse_main(response):
    zhihuhot = ZhihuHot()
    soup = BeautifulSoup(response, 'lxml')
    post_nodes = soup.select("div[class='Card TopstoryItem TopstoryItem-isRecommend']")
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
            file_name1 = "zhihuhotnews_%s.jpg" % curr_num_of_neim
            file_path1 = os.path.join("D:\StefanClub\StefanClub\www\static\img\zhihu", file_name1)
            urllib.request.urlretrieve(newsimgsrcurl, file_path1)
            zhihuhot["newsimgsrcurl"] = "../static/img/zhihu/%s" % file_name1
            zhihuhot["newsimgnumber"] = curr_num_of_neim
            curr_num_of_neim = curr_num_of_neim + 1

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
        file_name = "zhihuhotuser_%s.jpg" % curr_num_of_usim
        file_path = os.path.join("D:\StefanClub\StefanClub\www\static\img\zhihu", file_name)
        urllib.request.urlretrieve(userimgsrcurl, file_path)
        zhihuhot["userimgsrcurl"] = "../static/img/zhihu/%s" % file_name
        zhihuhot["userimgnumber"] = curr_num_of_usim
        curr_num_of_usim = curr_num_of_usim + 1

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
            if duplicate_record.process_item(zhihuhot) is not None:
                if redis_deduplicate.process_item(zhihuhot) is not None:
                    if inserttomysql.process_item(zhihuhot) == 'toinsert':
                        if hottype == 'question':
                            for i in range(comment_page):
                                html = s.get(answer_comment_url.format(hotid=hotid, offset=i * 20)).text
                                parse_zhihuhot_comment(html,hotid)
                        elif hottype == 'zhuanlan':
                            for i in range(comment_page):
                                html = s.get(zhuanlan_comment_url.format(hotid=hotid, offset=i * 20)).text
                                parse_zhihuhot_comment(html, hotid)
                        mainhtml = s.get(titleurl).text
                        parse_zhihuhot_content(mainhtml,hotid,hottype)


def parse_zhihuhot_comment(response,hotid):
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
        file_name = "zhihuhotcomuser_%s.jpg" % curr_num_of_comuser
        file_path = os.path.join("D:\StefanClub\StefanClub\www\static\img\zhihu", file_name)
        urllib.request.urlretrieve(userimgsrcurl, file_path)
        comment_item["userimgsrcurl"] = "../static/img/zhihu/%s" % file_name
        comment_item["userimgnumber"] = curr_num_of_comuser
        curr_num_of_comuser = curr_num_of_comuser + 1
        comment_item["commentid"] = commentid
        comment_item["hotid"] = hotid
        comment_item["userimgurl"] = userimgurl
        comment_item["username"] = username
        comment_item["replytouser"] = replytouser
        comment_item["replytouserurl"] = replytouserurl
        comment_item["replytime"] = replytime
        comment_item["content"] = content
        comment_item["infavorqty"] = infavorqty
        if duplicate_record.process_item(comment_item) is not None:
            if redis_deduplicate.process_item(comment_item) is not None:
                inserttomysql.process_item(comment_item)


def parse_zhihuhot_content(response,hotid,hottype):
    partno = 1
    zhihuhot_content = ZhihuHotContent()
    soup = BeautifulSoup(response, 'lxml')
    if hottype == 'question':
        post_node = soup.select("span[class='CopyrightRichText-richText']")
    else:
        post_node = soup.select("div[class='Post-RichText']")
    sel = Selector(text=str(post_node), type="html", )
    test = sel.xpath('*')


start_requests()
