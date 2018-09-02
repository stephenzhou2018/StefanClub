# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StefanclubscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class IndexCarouselItem(scrapy.Item):
    number = scrapy.Field()
    title = scrapy.Field()
    img_url = scrapy.Field()
    url = scrapy.Field()
    item_class = scrapy.Field()


class IndexNews(scrapy.Item):
    number = scrapy.Field()
    close_target_id = scrapy.Field()
    close_target_id_ref = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    news_summary = scrapy.Field()
    user_img_url = scrapy.Field()
    user_name = scrapy.Field()
    news_date = scrapy.Field()
    news_label = scrapy.Field()
    news_reads = scrapy.Field()
    news_comments = scrapy.Field()
    user_url = scrapy.Field()
    label_url = scrapy.Field()
    comment_url = scrapy.Field()


class HotMatches(scrapy.Item):
    livecast_id = scrapy.Field()
    type = scrapy.Field()
    title = scrapy.Field()
    team1 = scrapy.Field()
    team2 = scrapy.Field()
    score1 = scrapy.Field()
    score2 = scrapy.Field()
    matchdate = scrapy.Field()
    matchtime = scrapy.Field()
    newsurl = scrapy.Field()
    liveurl = scrapy.Field()
    match_url = scrapy.Field()


class SinaCarousel(scrapy.Item):
    number = scrapy.Field()
    title = scrapy.Field()
    img_url = scrapy.Field()
    url = scrapy.Field()


class HotMatchNews(scrapy.Item):
    number = scrapy.Field()
    title1 = scrapy.Field()
    title2 = scrapy.Field()
    title3 = scrapy.Field()
    title1url = scrapy.Field()
    title2url = scrapy.Field()
    title3url = scrapy.Field()
    imgsrcurl = scrapy.Field()
    imgurl = scrapy.Field()
    line1 = scrapy.Field()
    line2 = scrapy.Field()
    line3 = scrapy.Field()
    line4 = scrapy.Field()
    line5 = scrapy.Field()
    line6 = scrapy.Field()
    line7 = scrapy.Field()
    line8 = scrapy.Field()
    line9 = scrapy.Field()
    line1url = scrapy.Field()
    line2url = scrapy.Field()
    line3url = scrapy.Field()
    line4url = scrapy.Field()
    line5url = scrapy.Field()
    line6url = scrapy.Field()
    line7url = scrapy.Field()
    line8url = scrapy.Field()
    line9url = scrapy.Field()


class NbaNews(scrapy.Item):
    newstype = scrapy.Field()
    number = scrapy.Field()
    imgsrcurl = scrapy.Field()
    imgurl = scrapy.Field()
    isvideo = scrapy.Field()
    title = scrapy.Field()
    titleurl = scrapy.Field()
    newstime = scrapy.Field()
    comment_url = scrapy.Field()
    tag1 = scrapy.Field()
    tag2 = scrapy.Field()
    tag3 = scrapy.Field()
    tag4 = scrapy.Field()
    tag5 = scrapy.Field()
    tag1url = scrapy.Field()
    tag2url = scrapy.Field()
    tag3url = scrapy.Field()
    tag4url = scrapy.Field()
    tag5url = scrapy.Field()

