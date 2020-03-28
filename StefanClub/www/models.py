#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Models for user, blog, comment.
'''

__author__ = 'Stephen Zhou'

import time, uuid

from orm import Model, StringField, BooleanField, FloatField, TextField, IntegerField, DateTimeField


def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


class User(Model):
    __table__ = 'users'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    email = StringField(ddl='varchar(50)')
    passwd = StringField(ddl='varchar(50)')
    admin = BooleanField()
    name = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(default=time.time)


class Blog(Model):
    __table__ = 'blogs'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    name = StringField(ddl='varchar(50)')
    summary = StringField(ddl='varchar(200)')
    content = TextField()
    created_at = FloatField(default=time.time)


class Comment(Model):
    __table__ = 'comments'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    blog_id = StringField(ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    content = TextField()
    created_at = FloatField(default=time.time)


class IndexCarouselItems(Model):
    __table__ = 'IndexCarouselItems'

    id = IntegerField(primary_key=True)
    title = StringField(ddl='varchar(300)')
    url = StringField(ddl='varchar(300)')
    img_url = StringField(ddl='varchar(300)')
    item_class = StringField(ddl='varchar(10)')
    created_at = DateTimeField()


class IndexNews(Model):
    __table__ = 'IndexNews'

    id = IntegerField(primary_key=True)
    close_target_id = StringField(ddl='varchar(20)')
    close_target_id_ref = StringField(ddl='varchar(20)')
    title = StringField(ddl='varchar(300)')
    url = StringField(ddl='varchar(300)')
    news_summary = StringField(ddl='varchar(300)')
    user_img_url = StringField(ddl='varchar(300)')
    user_name = StringField(ddl='varchar(50)')
    news_date = StringField(ddl='varchar(100)')
    news_label = StringField(ddl='varchar(50)')
    news_reads = IntegerField()
    news_comments = IntegerField()
    hate_emails = StringField(ddl='varchar(3000)')
    user_url = StringField(ddl='varchar(300)')
    label_url = StringField(ddl='varchar(300)')
    comment_url = StringField(ddl='varchar(300)')
    created_at = DateTimeField()


class HotMatches(Model):
    __table__ = 'HotMatches'

    id = IntegerField(primary_key=True)
    type = StringField(ddl='varchar(50)')
    livecast_id = StringField(ddl='varchar(100)')
    title = StringField(ddl='varchar(300)')
    team1 = StringField(ddl='varchar(50)')
    team2 = StringField(ddl='varchar(50)')
    score1 = StringField(ddl='varchar(5)')
    score2 = StringField(ddl='varchar(5)')
    matchdate = StringField(ddl='varchar(100)')
    matchtime = StringField(ddl='varchar(100)')
    newsurl = StringField(ddl='varchar(300)')
    liveurl = StringField(ddl='varchar(300)')
    match_url = StringField(ddl='varchar(300)')
    created_at = DateTimeField()


class SinaCarousel(Model):
    __table__ = 'SinaCarousel'

    id = IntegerField(primary_key=True)
    title = StringField(ddl='varchar(300)')
    url = StringField(ddl='varchar(300)')
    img_url = StringField(ddl='varchar(300)')
    created_at = DateTimeField()


class HotMatchNews(Model):
    __table__ = 'HotMatchNews'

    id = IntegerField(primary_key=True)
    title1 = StringField(ddl='varchar(300)')
    title2 = StringField(ddl='varchar(300)')
    title3 = StringField(ddl='varchar(300)')
    title1url = StringField(ddl='varchar(300)')
    title2url = StringField(ddl='varchar(300)')
    title3url = StringField(ddl='varchar(300)')
    imgsrcurl = StringField(ddl='varchar(300)')
    imgurl = StringField(ddl='varchar(300)')
    line1 = StringField(ddl='varchar(300)')
    line2 = StringField(ddl='varchar(300)')
    line3 = StringField(ddl='varchar(300)')
    line4 = StringField(ddl='varchar(300)')
    line5 = StringField(ddl='varchar(300)')
    line6 = StringField(ddl='varchar(300)')
    line7 = StringField(ddl='varchar(300)')
    line8 = StringField(ddl='varchar(300)')
    line9 = StringField(ddl='varchar(300)')
    line1url = StringField(ddl='varchar(300)')
    line2url = StringField(ddl='varchar(300)')
    line3url = StringField(ddl='varchar(300)')
    line4url = StringField(ddl='varchar(300)')
    line5url = StringField(ddl='varchar(300)')
    line6url = StringField(ddl='varchar(300)')
    line7url = StringField(ddl='varchar(300)')
    line8url = StringField(ddl='varchar(300)')
    line9url = StringField(ddl='varchar(300)')
    created_at = DateTimeField()


class NbaNews(Model):
    __table__ = 'NbaNews'

    id = IntegerField(primary_key=True)
    imgsrcurl = StringField(ddl='varchar(300)')
    imgurl = StringField(ddl='varchar(300)')
    isvideo = StringField(ddl='varchar(5)')
    title = StringField(ddl='varchar(300)')
    titleurl = StringField(ddl='varchar(300)')
    newstime = DateTimeField()
    comment_url = StringField(ddl='varchar(300)')
    tag1 = StringField(ddl='varchar(300)')
    tag2 = StringField(ddl='varchar(300)')
    tag3 = StringField(ddl='varchar(300)')
    tag4 = StringField(ddl='varchar(300)')
    tag5 = StringField(ddl='varchar(300)')
    tag1url = StringField(ddl='varchar(300)')
    tag2url = StringField(ddl='varchar(300)')
    tag3url = StringField(ddl='varchar(300)')
    tag4url = StringField(ddl='varchar(300)')
    tag5url = StringField(ddl='varchar(300)')
    created_at = DateTimeField()
    
    
class ZhihuHot(Model):
    __table__ = 'ZhihuHot'

    id = IntegerField(primary_key=True)
    hotid = StringField(ddl='varchar(30)')
    collapse_no = StringField(ddl='varchar(20)')
    collapse_no_ref = StringField(ddl='varchar(20)')
    feedsourcetag = StringField(ddl='varchar(100)')
    feedsourceurl = StringField(ddl='varchar(300)')
    userimgnumber = IntegerField()
    userimgsrcurl = StringField(ddl='varchar(300)')
    userimgurl = StringField(ddl='varchar(300)')
    username = StringField(ddl='varchar(100)')
    userinfo = StringField(ddl='varchar(300)')
    newsimgnumber = IntegerField()
    newsimgsrcurl = StringField(ddl='varchar(300)')
    newsimgurl = StringField(ddl='varchar(300)')
    isvideo = StringField(ddl='varchar(5)')
    title = StringField(ddl='varchar(300)')
    titleurl = StringField(ddl='varchar(300)')
    newscontent = StringField(ddl='varchar(1000)')
    infavorqty  = StringField(ddl='varchar(20)')
    comment_url = StringField(ddl='varchar(300)')
    comment_title = StringField(ddl='varchar(300)')
    share_url = StringField(ddl='varchar(300)')
    created_at = DateTimeField()


class ZhihuHotComment(Model):
    __table__ = 'ZhihuHot_Comment'

    id = IntegerField(primary_key=True)
    commentid = StringField(ddl='varchar(30)')
    hotid = StringField(ddl='varchar(30)')
    userimgnumber = IntegerField()
    userimgsrcurl = StringField(ddl='varchar(300)')
    userimgurl = StringField(ddl='varchar(300)')
    username = StringField(ddl='varchar(100)')
    replytouser = StringField(ddl='varchar(100)')
    replytouserurl = StringField(ddl='varchar(300)')
    replytime = StringField(ddl='varchar(50)')
    content = StringField(ddl='varchar(1000)')
    infavorqty  = StringField(ddl='varchar(20)')
    created_at = DateTimeField()
    
    
class TaobaoProducts(Model):
    __table__ = 'TaobaoProducts'

    id = IntegerField(primary_key=True)
    keyword = StringField(ddl='varchar(30)')
    product_id = StringField(ddl='varchar(100)')
    product_type = StringField(ddl='varchar(100)')
    imgsrcurl = StringField(ddl='varchar(300)')
    imgurl = StringField(ddl='varchar(300)')
    imgnumber = IntegerField()
    samestyleurl = StringField(ddl='varchar(300)')
    similarurl = StringField(ddl='varchar(300)')
    product_price = StringField(ddl='varchar(20)')
    payednum  = StringField(ddl='varchar(20)')
    title = StringField(ddl='varchar(300)')
    title1 = StringField(ddl='varchar(300)')
    title2 = StringField(ddl='varchar(300)')
    titlehaskey = StringField(ddl='varchar(10)')
    titleurl = StringField(ddl='varchar(300)')
    shopname = StringField(ddl='varchar(100)')
    shopurl = StringField(ddl='varchar(300)')
    shopaddress = StringField(ddl='varchar(20)')
    shoplevelzuanqty = IntegerField()
    shoplevelguanqty = IntegerField()
    shoplevelxinqty = IntegerField()
    shopleveljingguanqty = IntegerField()
    istmall = StringField(ddl='varchar(10)')
    iconkey1 = StringField(ddl='varchar(100)')
    icontitle1 = StringField(ddl='varchar(100)')
    iconurl1 = StringField(ddl='varchar(300)')
    iconkey2 = StringField(ddl='varchar(100)')
    icontitle2 = StringField(ddl='varchar(100)')
    iconurl2 = StringField(ddl='varchar(300)')
    iconkey3 = StringField(ddl='varchar(100)')
    icontitle3 = StringField(ddl='varchar(100)')
    iconurl3 = StringField(ddl='varchar(300)')
    iconkey4 = StringField(ddl='varchar(100)')
    icontitle4 = StringField(ddl='varchar(100)')
    iconurl4 = StringField(ddl='varchar(300)')
    iconkey5 = StringField(ddl='varchar(100)')
    icontitle5 = StringField(ddl='varchar(100)')
    iconurl5 = StringField(ddl='varchar(300)')
    subiconclass1 = StringField(ddl='varchar(100)')
    subicontitle1 = StringField(ddl='varchar(100)')
    subiconcontent1 = StringField(ddl='varchar(300)')
    subiconclass2 = StringField(ddl='varchar(100)')
    subicontitle2 = StringField(ddl='varchar(100)')
    subiconcontent2 = StringField(ddl='varchar(300)')
    subiconclass3 = StringField(ddl='varchar(100)')
    subicontitle3 = StringField(ddl='varchar(100)')
    subiconcontent3 = StringField(ddl='varchar(300)')
    subiconclass4 = StringField(ddl='varchar(100)')
    subicontitle4 = StringField(ddl='varchar(100)')
    subiconcontent4 = StringField(ddl='varchar(300)')
    subiconclass5 = StringField(ddl='varchar(100)')
    subicontitle5 = StringField(ddl='varchar(100)')
    subiconcontent5 = StringField(ddl='varchar(300)')
    shoptotalrate = StringField(ddl='varchar(20)')
    shopdescscore = StringField(ddl='varchar(20)')
    shopdescscorediff = StringField(ddl='varchar(20)')
    shopdesccompare = StringField(ddl='varchar(20)')
    shopdeliveryscore = StringField(ddl='varchar(20)')
    shopdeliveryscorediff = StringField(ddl='varchar(20)')
    shopdeliverycompare = StringField(ddl='varchar(20)')
    shopservicescore = StringField(ddl='varchar(20)')
    shopservicescorediff = StringField(ddl='varchar(20)')
    shopservicecompare = StringField(ddl='varchar(20)')
    product_price_float = FloatField()
    product_sales_qty = IntegerField()
    shop_ave_score = FloatField()
    created_at = DateTimeField()


class ZhihuHotContent(Model):
    __table__ = 'ZhihuHot_Content'

    id = IntegerField(primary_key=True)
    hotid = StringField(ddl='varchar(30)')
    partno = IntegerField()
    parttype = StringField(ddl='varchar(30)')
    imgurl = StringField(ddl='varchar(300)')
    imgnumber = IntegerField()
    videourl = StringField(ddl='varchar(300)')
    text = TextField()
    created_at = DateTimeField()


class ZhaoPinJobs(Model):
    __table__ = 'ZhaoPinJobs'

    id = IntegerField(primary_key=True)
    source = StringField(ddl='varchar(30)')
    jobkey = StringField(ddl='varchar(30)')
    jobid = StringField(ddl='varchar(30)')
    jobtitle = StringField(ddl='varchar(100)')
    salarystr = StringField(ddl='varchar(100)')
    salary_month_min = IntegerField()
    salary_year_min = IntegerField()
    salary_month_max = IntegerField()
    salary_year_max = IntegerField()
    address = StringField(ddl='varchar(300)')
    education = StringField(ddl='varchar(100)')
    workexperience = StringField(ddl='varchar(50)')
    release_time = StringField(ddl='varchar(100)')
    response_time = StringField(ddl='varchar(100)')
    companyname = StringField(ddl='varchar(200)')
    industry = StringField(ddl='varchar(200)')
    financing_situation = StringField(ddl='varchar(100)')
    numberofpeople = StringField(ddl='varchar(100)')
    welfare1 = StringField(ddl='varchar(100)')
    welfare2 = StringField(ddl='varchar(100)')
    welfare3 = StringField(ddl='varchar(100)')
    welfare4 = StringField(ddl='varchar(100)')
    welfare5 = StringField(ddl='varchar(100)')
    created_at = DateTimeField()