# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import datetime
from items import IndexCarouselItem,IndexNews,HotMatches,SinaCarousel,HotMatchNews,NbaNews,ZhihuHot
from scrapy.exceptions import DropItem
from redis import Redis
import pandas as pd



class StefanclubscrapyPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    '''
    插入mysql数据库
    '''
    def __init__(self):
        self.conn =pymysql.connect(host='localhost',port=3306,user='root',passwd='Kaihua1010',db='stefan',use_unicode=True, charset="utf8")
        self.cursor = self.conn.cursor()

    def process_item(self,item,spider):
        if isinstance(item, IndexCarouselItem):
            insert_sql = '''
            insert into IndexCarouselItems(number,title,url,img_url,item_class,created_at) VALUES (%s,%s,%s,%s,%s,%s)
            '''
            self.cursor.execute(insert_sql, (item["number"],item["title"], item["url"], item["img_url"], item["item_class"],
                                             datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        elif isinstance(item, IndexNews):
            insert_sql = '''
            insert into IndexNews(number,close_target_id,close_target_id_ref,title,url,news_summary,user_img_url,user_name,news_date,news_label,news_reads,news_comments,hate_emails,created_at,user_url,label_url,comment_url) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
            self.cursor.execute(insert_sql, (
            item["number"],item["close_target_id"], item["close_target_id_ref"], item["title"], item["url"], item["news_summary"],
            item["user_img_url"], item["user_name"], item["news_date"], item["news_label"], item["news_reads"],
            item["news_comments"], '', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), item["user_url"],
            item["label_url"], item["comment_url"]))

        elif isinstance(item, HotMatches):
            insert_sql = '''
            insert into HotMatches(livecast_id,type,title,team1,team2,score1,score2,matchdate,matchtime,newsurl,liveurl,match_url,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
            self.cursor.execute(insert_sql, (item["livecast_id"],
            item["type"], item["title"], item["team1"], item["team2"], item["score1"],
            item["score2"], item["matchdate"], item["matchtime"], item["newsurl"], item["liveurl"],
            item["match_url"], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        elif isinstance(item, SinaCarousel):
            insert_sql = '''
            insert into SinaCarousel(number,title,url,img_url,created_at) VALUES (%s,%s,%s,%s,%s)
            '''
            self.cursor.execute(insert_sql, (item["number"],item["title"], item["url"], item["img_url"],
                                             datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        elif isinstance(item, HotMatchNews):
            insert_sql = '''
            insert into HotMatchNews(number,title1,title2,title3,title1url,title2url,title3url,imgsrcurl,imgurl,line1,
            line2,line3,line4,line5,line6,line7,line8,line9,line1url,line2url,line3url,line4url,line5url,line6url,
            line7url,line8url,line9url,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
            self.cursor.execute(insert_sql, (
            item["number"],item["title1"], item["title2"], item["title3"], item["title1url"], item["title2url"],
            item["title3url"], item["imgsrcurl"], item["imgurl"], item["line1"], item["line2"],
            item["line3"],item["line4"], item["line5"],item["line6"], item["line7"],item["line8"], item["line9"],
            item["line1url"], item["line2url"],item["line3url"],item["line4url"], item["line5url"],item["line6url"],
            item["line7url"],item["line8url"], item["line9url"], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        elif isinstance(item, NbaNews):
            insert_sql = '''
            insert into NbaNews(newstype,number,imgsrcurl,imgurl,isvideo,title,titleurl,newstime,comment_url,tag1,tag2,tag3,tag4,
            tag5,tag1url,tag2url,tag3url,tag4url,tag5url,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s)
            '''
            self.cursor.execute(insert_sql, (
            item["newstype"],item["number"], item["imgsrcurl"], item["imgurl"], item["isvideo"], item["title"],item["titleurl"],item["newstime"],
            item["comment_url"],item["tag1"], item["tag2"],item["tag3"], item["tag4"],item["tag5"], item["tag1url"],item["tag2url"],
            item["tag3url"], item["tag4url"],item["tag5url"],datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        elif isinstance(item, ZhihuHot):
            insert_sql = '''
            insert into ZhihuHot(feedsourcetag,feedsourceurl,userimgnumber,userimgsrcurl,userimgurl,username,userinfo,
            newsimgnumber,newsimgsrcurl,newsimgurl,isvideo,title,titleurl,newscontent,infavorqty,comment_url,comment_title,
            share_url,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
            self.cursor.execute(insert_sql, (
            item["feedsourcetag"],item["feedsourceurl"], item["userimgnumber"], item["userimgsrcurl"], item["userimgurl"], item["username"],item["userinfo"],item["newsimgnumber"],
            item["newsimgsrcurl"],item["newsimgurl"], item["isvideo"],item["title"], item["titleurl"],item["newscontent"], item["infavorqty"],item["comment_url"],
            item["comment_title"], item["share_url"],datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

        else:
            pass
        self.conn.commit()
        return item


class DuplicatesPipeline(object):
    def __init__(self):
        self.livecast_ids_seen = set()
        self.carurls_seen = set()
        self.newsurls_seen = set()
        self.sinacar_seen = set()
        self.hotmatchnews_seen = set()
        self.nbanews_seen = set()
        self.zhihuhot_seen = set()

    def process_item(self, item, spider):
        if isinstance(item, HotMatches):
            if item['livecast_id'] in self.livecast_ids_seen:
                raise DropItem("(Scrapy)Duplicate item found: %s" % item)
            else:
                self.livecast_ids_seen.add(item['livecast_id'])
                return item

        elif isinstance(item, IndexCarouselItem):
            if item['url'] in self.carurls_seen:
                raise DropItem("(Scrapy)Duplicate item found: %s" % item)
            else:
                self.carurls_seen.add(item['url'])
                return item

        elif isinstance(item, IndexNews):
            if item['url'] in self.newsurls_seen:
                raise DropItem("(Scrapy)Duplicate item found: %s" % item)
            else:
                self.newsurls_seen.add(item['url'])
                return item

        elif isinstance(item, SinaCarousel):
            if item['url'] in self.sinacar_seen:
                raise DropItem("(Scrapy)Duplicate item found: %s" % item)
            else:
                self.sinacar_seen.add(item['url'])
                return item

        elif isinstance(item, HotMatchNews):
            if item['imgsrcurl'] in self.hotmatchnews_seen:
                raise DropItem("(Scrapy)Duplicate item found: %s" % item)
            else:
                self.hotmatchnews_seen.add(item['imgsrcurl'])
                return item

        elif isinstance(item, NbaNews):
            if item['title'] in self.nbanews_seen:
                raise DropItem("(Scrapy)Duplicate item found: %s" % item)
            else:
                self.nbanews_seen.add(item['title'])
                return item

        elif isinstance(item, ZhihuHot):
            if item['title'] in self.zhihuhot_seen:
                raise DropItem("(Scrapy)Duplicate item found: %s" % item)
            else:
                self.zhihuhot_seen.add(item['title'])
                return item

        else:
            return item



redis_db = Redis(host='127.0.0.1', port=6379, db=0) #连接redis
redis_data_dict = "k_livecastid"
redis_data_dict1 = "k_carurls"
redis_data_dict2 = "k_newsurls"
redis_data_dict3 = "k_sinacarurls"
redis_data_dict4 = "k_hotmatnews_imgurls"
redis_data_dict5 = "k_nbanews_titles"
redis_data_dict6 = "k_zhihuhot_titles"



class RedisPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(host='localhost',port=3306,user='root',passwd='Kaihua1010',db='stefan',use_unicode=True, charset="utf8")
        self.cursor = self.connect.cursor()
        redis_db.flushdb()

        if redis_db.hlen(redis_data_dict) == 0:
            sql = "SELECT livecast_id FROM HotMatches;"
            df = pd.read_sql(sql, self.connect)
            for livecast_id in df['livecast_id'].get_values():
                redis_db.hset(redis_data_dict, livecast_id, 0)

        if redis_db.hlen(redis_data_dict1) == 0:
            sql = "SELECT url FROM indexcarouselitems;"
            df = pd.read_sql(sql, self.connect)
            for car_url in df['url'].get_values():
                redis_db.hset(redis_data_dict1, car_url, 0)

        if redis_db.hlen(redis_data_dict2) == 0:
            sql = "SELECT url FROM indexnews;"
            df = pd.read_sql(sql, self.connect)
            for news_url in df['url'].get_values():
                redis_db.hset(redis_data_dict2, news_url, 0)

        if redis_db.hlen(redis_data_dict3) == 0:
            sql = "SELECT url FROM SinaCarousel;"
            df = pd.read_sql(sql, self.connect)
            for sinacar_url in df['url'].get_values():
                redis_db.hset(redis_data_dict3, sinacar_url, 0)

        if redis_db.hlen(redis_data_dict4) == 0:
            sql = "SELECT imgsrcurl FROM HotMatchNews;"
            df = pd.read_sql(sql, self.connect)
            for hot_img_url in df['imgsrcurl'].get_values():
                redis_db.hset(redis_data_dict4, hot_img_url, 0)

        if redis_db.hlen(redis_data_dict5) == 0:
            sql = "SELECT title FROM NbaNews;"
            df = pd.read_sql(sql, self.connect)
            for nba_title in df['title'].get_values():
                redis_db.hset(redis_data_dict5, nba_title, 0)

        if redis_db.hlen(redis_data_dict6) == 0:
            sql = "SELECT title FROM ZhihuHot;"
            df = pd.read_sql(sql, self.connect)
            for zhihuhot_title in df['title'].get_values():
                redis_db.hset(redis_data_dict6, zhihuhot_title, 0)


    def process_item(self, item, spider):
        if isinstance(item, HotMatches):
            if redis_db.hexists (redis_data_dict, item['livecast_id']):
                raise DropItem("(Redis)Duplicate item found: %s" % item)
            else:
                return item

        elif isinstance(item, IndexCarouselItem):
            if redis_db.hexists (redis_data_dict1, item['url']):
                raise DropItem("(Redis)Duplicate item found: %s" % item)
            else:
                return item

        elif isinstance(item, IndexNews):
            if redis_db.hexists (redis_data_dict2, item['url']):
                raise DropItem("(Redis)Duplicate item found: %s" % item)
            else:
                return item

        elif isinstance(item, SinaCarousel):
            if redis_db.hexists (redis_data_dict3, item['url']):
                raise DropItem("(Redis)Duplicate item found: %s" % item)
            else:
                return item

        elif isinstance(item, HotMatchNews):
            if redis_db.hexists (redis_data_dict4, item['imgsrcurl']):
                raise DropItem("(Redis)Duplicate item found: %s" % item)
            else:
                return item

        elif isinstance(item, NbaNews):
            if redis_db.hexists (redis_data_dict5, item['title']):
                raise DropItem("(Redis)Duplicate item found: %s" % item)
            else:
                return item

        elif isinstance(item, ZhihuHot):
            if redis_db.hexists (redis_data_dict6, item['title']):
                raise DropItem("(Redis)Duplicate item found: %s" % item)
            else:
                return item

        else:
            return item




class MysqlUpdatePipeline(object):

    def __init__(self):
        self.conn =pymysql.connect(host='localhost',port=3306,user='root',passwd='Kaihua1010',db='stefan',use_unicode=True, charset="utf8")
        self.cursor = self.conn.cursor()

    def process_item(self,item,spider):
        if isinstance(item, IndexNews):
            update_sql = '''
               update IndexNews set close_target_id = concat(left(close_target_id, 8),concat(id)) , close_target_id_ref = concat(left(close_target_id_ref, 9),concat(id));
             '''
        elif isinstance(item, ZhihuHot):
            update_sql = '''
               update ZhihuHot set collapse_no = concat('collapse',concat(id)) , collapse_no_ref = concat('#collapse',concat(id));
             '''
        else:
            update_sql = None
        if update_sql is not None:
            self.cursor.execute(update_sql)
            self.conn.commit()


def get_max_num(num_type,indexcar_type=None):
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='Kaihua1010', db='stefan',
                           use_unicode=True, charset="utf8")
    cursor = conn.cursor()
    select_sql = ''
    if num_type == 'index_news':
        select_sql = '''
            select max(number) from IndexNews
             '''
    elif num_type == 'index_car':
        select_sql = '''
            select max(number) from IndexCarouselItems where item_class = "''' + indexcar_type + '''"'''
    elif num_type == 'sinacar':
        select_sql = '''
            select max(number) from SinaCarousel
             '''
    elif num_type == 'hotmatch_news':
        select_sql = '''
            select max(number) from HotMatchNews
             '''
    elif num_type == 'nbanews':
        select_sql = '''
            select max(number) from NbaNews where newstype <> 'lefttop' and newstype <> 'lefttoplines' 
            and newstype <> 'leftsec' and newstype <> 'leftsectxt'
             '''
    elif num_type == 'lefttop':
        select_sql = '''
            select max(number) from NbaNews where newstype = 'lefttop' 
             '''
    elif num_type == 'leftsec':
        select_sql = '''
            select max(number) from NbaNews where newstype = 'leftsec' 
             '''
    elif num_type == 'zhihuhotuser':
        select_sql = '''
            select max(userimgnumber) from zhihuhot 
             '''
    elif num_type == 'zhihuhotnews':
        select_sql = '''
            select max(newsimgnumber) from zhihuhot 
             '''
    else:
        pass

    cursor.execute(select_sql)
    rs = cursor.fetchone()
    return rs[0]