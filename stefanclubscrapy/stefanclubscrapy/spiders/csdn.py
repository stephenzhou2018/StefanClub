# -*- coding: utf-8 -*-
import scrapy,json
import sys,os,urllib.request
sys.path.append('D:\StefanClub\stefanclubscrapy\stefanclubscrapy')
from items import IndexCarouselItem,IndexNews
from bs4 import BeautifulSoup
from scrapy import Selector,Request
from pipelines import get_max_num


class CsdnSpider(scrapy.Spider):
    name = 'csdn'
    allowed_domains = ["www.csdn.net"]
    start_urls = ['http://www.csdn.net/']

    index_url = 'http://www.csdn.net/'
    more_artice_url = 'https://www.csdn.net/api/articles?type=more&category=home&shown_offset={shown_offset}'

    max_index_news_num = get_max_num('index_news')
    if max_index_news_num is None:
        max_index_news_num = 0
    curr_num_of_article = max_index_news_num + 1

    max_car_number = get_max_num('index_car','Carousel')
    if max_car_number is None:
        max_car_number = 0
    curr_num_of_car = max_car_number + 1

    max_car_r_number = get_max_num('index_car','Carousel_R')
    if max_car_r_number is None:
        max_car_r_number = 0
    curr_num_of_car_r = max_car_r_number + 1

    max_right_number = get_max_num('index_car','Right')
    if max_right_number is None:
        max_right_number = 0
    curr_num_of_right = max_right_number + 1

    def start_requests(self):
        yield Request(self.index_url, callback=self.parse_index)
        for i in range(1, 5):
            yield Request(self.more_artice_url.format(shown_offset=21+(i-1)*10),callback=self.parse_more_index_art)


    def parse_index(self, response):
        carousel_item = IndexCarouselItem()
        index_news_item  = IndexNews()
        soup = BeautifulSoup(response.text, 'lxml')
        post_nodes = soup.select(".carousel-inner .csdn-tracking-statistics")
        post_nodes1 = soup.select(".carousel-right .carousel-right-u")
        post_nodes2 = soup.select(".company_list li")
        post_nodes3 = soup.select(".feedlist_mod li[class='clearfix'] div[class='list_con']")
        for post_node in post_nodes:
            sel = Selector(text=str(post_node), type="html", )
            title = sel.xpath('//div[@class="carousel-caption"]/text()').extract()[0].strip()
            url = sel.xpath('//a//@href').extract()[0].strip()
            img_url = sel.xpath('//img//@src').extract()[0].strip()
            file_name = "carousel_%s.jpg" % (self.curr_num_of_car)
            file_path = os.path.join("D:\StefanClub\StefanClub\www\static\img\csdn", file_name)
            urllib.request.urlretrieve(img_url, file_path)

            carousel_item["number"] = self.curr_num_of_car
            self.curr_num_of_car = self.curr_num_of_car + 1
            carousel_item["title"] = title
            carousel_item["url"] = url
            #carousel_item["img_url"] = img_url
            carousel_item["img_url"] = "../static/img/csdn/%s" % (file_name)
            carousel_item["item_class"] = "Carousel"
            yield carousel_item

        for post_node1 in post_nodes1:
            sel1 = Selector(text=str(post_node1), type="html", )
            title1 = sel1.xpath('//p[@class="carousel-right-caption"]/span/text()').extract()[0].strip()
            url1 = sel1.xpath('//a//@href').extract()[0].strip()
            img_url1 = sel1.xpath('//img//@src').extract()[0].strip()
            file_name1 = "carousel_right_%s.jpg" % (self.curr_num_of_car_r)
            file_path1 = os.path.join("D:\StefanClub\StefanClub\www\static\img\csdn", file_name1)
            urllib.request.urlretrieve(img_url1, file_path1)

            carousel_item["number"] = self.curr_num_of_car_r
            self.curr_num_of_car_r = self.curr_num_of_car_r + 1
            carousel_item["title"] = title1
            carousel_item["url"] = url1
            #carousel_item["img_url"] = img_url
            carousel_item["img_url"] = "../static/img/csdn/%s" % (file_name1)
            carousel_item["item_class"] = "Carousel_R"
            yield carousel_item

        for post_node2 in post_nodes2:
            sel2 = Selector(text=str(post_node2), type="html", )
            title2 = sel2.xpath('//h3/a/text()').extract()[0].strip()
            url2 = sel2.xpath('//h3/a//@href').extract()[0].strip()
            img_url2 = sel2.xpath('//img//@src').extract()[0].strip()
            file_name2 = "right_%s.jpg" % (self.curr_num_of_right)
            file_path2 = os.path.join("D:\StefanClub\StefanClub\www\static\img\csdn", file_name2)
            urllib.request.urlretrieve(img_url2, file_path2)

            carousel_item["number"] = self.curr_num_of_right
            self.curr_num_of_right = self.curr_num_of_right + 1
            carousel_item["title"] = title2
            carousel_item["url"] = url2
            # carousel_item["img_url"] = img_url
            carousel_item["img_url"] = "../static/img/csdn/%s" % (file_name2)
            carousel_item["item_class"] = "Right"
            yield carousel_item

        for post_node3 in post_nodes3:
            sel3 = Selector(text=str(post_node3), type="html", )
            index_news_item["close_target_id"]  = "myModal_%s" % (self.curr_num_of_article)
            index_news_item["close_target_id_ref"] = "#myModal_%s" % (self.curr_num_of_article)
            title3 = sel3.xpath('//div[@class="title"]/h2/a/text()').extract()[0].strip()
            url3 = sel3.xpath('//div[@class="title"]/h2/a//@href').extract()[0].strip()
            news_summary = sel3.xpath('//div[@class="summary oneline"]/text()').extract()[0].strip()
            user_url = sel3.xpath('//dt/a//@href').extract()[0].strip()
            user_img_url = sel3.xpath('//dt/a/img//@src').extract()[0].strip()
            user_name =  sel3.xpath('//dd[@class="name"]/a/text()').extract()[0].strip()
            news_date = sel3.xpath('//dd[@class="time"]/text()').extract()[0].strip()
            label_url = ''
            news_label = ''
            news_reads = '0'
            news_comments = '0'
            label_list = sel3.xpath('//dd[@class="tag"]/a//@href')
            if len(label_list) > 0:
                label_url = sel3.xpath('//dd[@class="tag"]/a//@href').extract()[0].strip()

            label_list2 = sel3.xpath('//dd[@class="tag"]/a/text()')
            if len(label_list2) > 0:
                news_label = sel3.xpath('//dd[@class="tag"]/a/text()').extract()[0].strip()

            reads_num_list = sel3.xpath('//dd[@class="read_num"]/a/span[@class="num"]/text()')
            if len(reads_num_list) > 0:
                news_reads = sel3.xpath('//dd[@class="read_num"]/a/span[@class="num"]/text()').extract()[0].strip()
            comment_url = sel3.xpath('//dd[@class="common_num "]/a//@href').extract()[0].strip()
            comment_num_list = sel3.xpath('//dd[@class="common_num "]/a/span[@class="num"]/text()')
            if len(comment_num_list) > 0:
                news_comments = sel3.xpath('//dd[@class="common_num "]/a/span[@class="num"]/text()').extract()[0].strip()

            file_name3 = "userimg_%s.jpg" % (self.curr_num_of_article)
            index_news_item["number"] = self.curr_num_of_article
            self.curr_num_of_article = self.curr_num_of_article + 1
            file_path3 = os.path.join("D:\StefanClub\StefanClub\www\static\img\csdn", file_name3)
            urllib.request.urlretrieve(user_img_url, file_path3)

            index_news_item["title"] = title3
            index_news_item["url"] = url3
            index_news_item["news_summary"] = news_summary
            index_news_item["user_img_url"] = "../static/img/csdn/%s" % (file_name3)
            index_news_item["user_name"] = user_name
            index_news_item["user_url"] = user_url
            index_news_item["news_date"] = news_date
            index_news_item["label_url"] = label_url
            index_news_item["news_label"] = news_label
            index_news_item["news_reads"] = int(news_reads)
            index_news_item["comment_url"] = comment_url
            index_news_item["news_comments"] = int(news_comments)

            yield index_news_item


    def parse_more_index_art(self, response):
        resultjson = json.loads(response.body)
        articles = resultjson['articles']
        index_news_item  = IndexNews()
        for article in articles:
            title = article['title']
            url = article['url']
            news_summary = article['summary']
            user_img_url = article['avatar']
            close_target_id  = "myModal_%s" % (self.curr_num_of_article)
            close_target_id_ref = "#myModal_%s" % (self.curr_num_of_article)
            file_name = "userimg_%s.jpg" % (self.curr_num_of_article)
            index_news_item["number"] = self.curr_num_of_article
            self.curr_num_of_article = self.curr_num_of_article + 1
            file_path = os.path.join("D:\StefanClub\StefanClub\www\static\img\csdn", file_name)
            urllib.request.urlretrieve(user_img_url, file_path)
            user_name = article['user_name']
            user_url = article['user_url']
            news_date = article['created_at']
            news_label = article['category']
            label_url = "/nav/%s" % (article['category_id'])
            news_reads = article['views']
            news_comments = article['comments']
            comment_url = "%s#comment_form" % (article['url'])

            index_news_item["close_target_id"]  = close_target_id
            index_news_item["close_target_id_ref"] = close_target_id_ref
            index_news_item["title"] = title
            index_news_item["url"] = url
            index_news_item["news_summary"] = news_summary
            index_news_item["user_img_url"] = "../static/img/csdn/%s" % (file_name)
            index_news_item["user_name"] = user_name
            index_news_item["user_url"] = user_url
            index_news_item["news_date"] = news_date
            index_news_item["label_url"] = label_url
            index_news_item["news_label"] = news_label
            index_news_item["news_reads"] = news_reads
            index_news_item["comment_url"] = comment_url
            index_news_item["news_comments"] = news_comments

            yield index_news_item