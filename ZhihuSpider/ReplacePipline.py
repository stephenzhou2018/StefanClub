from items import ZhihuHot,ZhihuHotComment,ZhihuHotContent
import pymysql
import datetime
from redis import Redis
import pandas as pd


class InsertToMysql(object):
    '''
    插入mysql数据库
    '''
    def __init__(self):
        self.conn =pymysql.connect(host='localhost',port=3306,user='root',passwd='Kaihua1010',db='stefan',use_unicode=True, charset="utf8")
        self.cursor = self.conn.cursor()

    def process_item(self,item):
        final_result = None
        if isinstance(item, ZhihuHot):
            insert_sql = '''
            insert into ZhihuHot(hotid,feedsourcetag,feedsourceurl,userimgnumber,userimgsrcurl,userimgurl,username,userinfo,
            newsimgnumber,newsimgsrcurl,newsimgurl,isvideo,title,titleurl,newscontent,infavorqty,comment_url,comment_title,
            share_url,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
            self.cursor.execute(insert_sql, (
            item["hotid"],item["feedsourcetag"],item["feedsourceurl"], item["userimgnumber"], item["userimgsrcurl"], item["userimgurl"], item["username"],item["userinfo"],item["newsimgnumber"],
            item["newsimgsrcurl"],item["newsimgurl"], item["isvideo"],item["title"], item["titleurl"],item["newscontent"], item["infavorqty"],item["comment_url"],
            item["comment_title"], item["share_url"],datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            final_result = 'toinsert'

        elif isinstance(item, ZhihuHotComment):
            insert_sql = '''
            insert into ZhihuHot_Comment(commentid,hotid,userimgnumber,userimgsrcurl,userimgurl,username,replytouser,replytouserurl,replytime,
            content,infavorqty,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
            self.cursor.execute(insert_sql, (
            item["commentid"],item["hotid"],item["userimgnumber"],item["userimgsrcurl"], item["userimgurl"], item["username"], item["replytouser"], item["replytouserurl"],item["replytime"],item["content"],
            item["infavorqty"],datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            final_result = 'toinsert'

        elif isinstance(item, ZhihuHotContent):
            insert_sql = '''
            insert into ZhihuHot_Content(hotid,partno,parttype,imgurl,imgnumber,videourl,text,created_at) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            '''
            self.cursor.execute(insert_sql, (
            item["hotid"],item["partno"],item["parttype"],item["imgurl"], item["imgnumber"], item["videourl"], item["text"], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            final_result = 'toinsert'

        else:
            pass
        if final_result == 'toinsert':
            self.conn.commit()
            return final_result
        else:
            return final_result


class DuplicatesRecord(object):
    def __init__(self):
        self.zhihuhot_seen = set()
        self.zhihuhotcom_seen = set()
        self.zhihuhotcontentid_seen = set()
        self.zhihuhotcontentpart_seen = set()

    def process_item(self, item):
        if isinstance(item, ZhihuHot):
            if item['hotid'] in self.zhihuhot_seen:
                return None
            else:
                self.zhihuhot_seen.add(item['hotid'])
                return item

        elif isinstance(item, ZhihuHotComment):
            if item['commentid'] in self.zhihuhotcom_seen:
                return None
            else:
                self.zhihuhotcom_seen.add(item['commentid'])
                return item

        elif isinstance(item, ZhihuHotContent):
            if item['hotid'] in self.zhihuhotcontentid_seen and item['partno'] in self.zhihuhotcontentpart_seen:
                return None
            else:
                self.zhihuhotcontentid_seen.add(item['hotid'])
                self.zhihuhotcontentpart_seen.add(item['partno'])
                return item
        else:
            return item


redis_db = Redis(host='127.0.0.1', port=6379, db=0) #连接redis

redis_data_dict6 = "k_zhihuhot_hotids"
redis_data_dict7 = "k_zhihuhotcom_ids"
redis_data_dict9 = "k_zhihuhotcontent_ids"
redis_data_dict10 = "k_zhihuhotcontent_parts"


class RedisDeDuplicate(object):
    def __init__(self):
        self.connect = pymysql.connect(host='localhost',port=3306,user='root',passwd='Kaihua1010',db='stefan',use_unicode=True, charset="utf8")
        self.cursor = self.connect.cursor()
        redis_db.flushdb()

        if redis_db.hlen(redis_data_dict6) == 0:
            sql = "SELECT hotid FROM ZhihuHot;"
            df = pd.read_sql(sql, self.connect)
            for zhihuhot_hotid in df['hotid'].get_values():
                redis_db.hset(redis_data_dict6, zhihuhot_hotid, 0)
        if redis_db.hlen(redis_data_dict7) == 0:
            sql = "SELECT commentid FROM ZhihuHot_Comment;"
            df = pd.read_sql(sql, self.connect)
            for zhihuhotcom_id in df['commentid'].get_values():
                redis_db.hset(redis_data_dict7, zhihuhotcom_id, 0)
        if redis_db.hlen(redis_data_dict9) == 0:
            sql = "SELECT hotid FROM ZhihuHot_Content;"
            df = pd.read_sql(sql, self.connect)
            for hot_id in df['hotid'].get_values():
                redis_db.hset(redis_data_dict9, hot_id, 0)
        if redis_db.hlen(redis_data_dict10) == 0:
            sql = "SELECT partno FROM ZhihuHot_Content;"
            df = pd.read_sql(sql, self.connect)
            for part_no in df['partno'].get_values():
                redis_db.hset(redis_data_dict10, part_no, 0)

    def process_item(self, item):
        if isinstance(item, ZhihuHot):
            if redis_db.hexists (redis_data_dict6, item['hotid']):
                return None
            else:
                return item
        elif isinstance(item, ZhihuHotComment):
            if redis_db.hexists (redis_data_dict7, item['commentid']):
                return None
            else:
                return item
        elif isinstance(item, ZhihuHotContent):
            if redis_db.hexists (redis_data_dict9, item['hotid']) and redis_db.hexists (redis_data_dict10, item['partno']):
                return None
            else:
                return item
        else:
            return item


class UpdateCollapseNo(object):

    def __init__(self):
        self.conn =pymysql.connect(host='localhost',port=3306,user='root',passwd='Kaihua1010',db='stefan',use_unicode=True, charset="utf8")
        self.cursor = self.conn.cursor()

    def updatedata(self):
        update_sql = '''
               update ZhihuHot set collapse_no = concat('collapse',concat(id)) , collapse_no_ref = concat('#collapse',concat(id));
             '''
        self.cursor.execute(update_sql)
        self.conn.commit()