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
    
    
class ZhihuHot(scrapy.Item):
    hotid = scrapy.Field()
    feedsourcetag = scrapy.Field()
    feedsourceurl = scrapy.Field()
    userimgnumber = scrapy.Field()
    userimgsrcurl = scrapy.Field()
    userimgurl = scrapy.Field()
    username = scrapy.Field()
    userinfo = scrapy.Field()
    newsimgnumber = scrapy.Field()
    newsimgsrcurl = scrapy.Field()
    newsimgurl = scrapy.Field()
    isvideo = scrapy.Field()
    title = scrapy.Field()
    titleurl = scrapy.Field()
    newscontent = scrapy.Field()
    infavorqty  = scrapy.Field()
    comment_url = scrapy.Field()
    comment_title = scrapy.Field()
    share_url = scrapy.Field()


class ZhihuHotComment(scrapy.Item):
    commentid = scrapy.Field()
    hotid = scrapy.Field()
    userimgnumber = scrapy.Field()
    userimgsrcurl = scrapy.Field()
    userimgurl = scrapy.Field()
    username = scrapy.Field()
    replytouser = scrapy.Field()
    replytouserurl = scrapy.Field()
    replytime = scrapy.Field()
    content = scrapy.Field()
    infavorqty  = scrapy.Field()


class TaobaoProducts(scrapy.Item):
    keyword = scrapy.Field()
    product_id = scrapy.Field()
    imgsrcurl = scrapy.Field()
    imgurl = scrapy.Field()
    imgnumber = scrapy.Field()
    samestyleurl = scrapy.Field()
    similarurl = scrapy.Field()
    product_price = scrapy.Field()
    payednum  = scrapy.Field()
    title = scrapy.Field()
    title1 = scrapy.Field()
    title2 = scrapy.Field()
    titlehaskey = scrapy.Field()
    titleurl = scrapy.Field()
    shopname = scrapy.Field()
    shopurl = scrapy.Field()
    shopaddress = scrapy.Field()
    shoplevelzuanqty = scrapy.Field()
    shoplevelguanqty = scrapy.Field()
    shoplevelxinqty = scrapy.Field()
    shopleveljingguanqty = scrapy.Field()
    istmall = scrapy.Field()
    iconkey1 = scrapy.Field()
    icontitle1 = scrapy.Field()
    iconurl1 = scrapy.Field()
    iconkey2 = scrapy.Field()
    icontitle2 = scrapy.Field()
    iconurl2 = scrapy.Field()
    iconkey3 = scrapy.Field()
    icontitle3 = scrapy.Field()
    iconurl3 = scrapy.Field()
    iconkey4 = scrapy.Field()
    icontitle4 = scrapy.Field()
    iconurl4 = scrapy.Field()
    iconkey5 = scrapy.Field()
    icontitle5 = scrapy.Field()
    iconurl5 = scrapy.Field()
    subiconclass1 = scrapy.Field()
    subicontitle1 = scrapy.Field()
    subiconcontent1 = scrapy.Field()
    subiconclass2 = scrapy.Field()
    subicontitle2 = scrapy.Field()
    subiconcontent2 = scrapy.Field()
    subiconclass3 = scrapy.Field()
    subicontitle3 = scrapy.Field()
    subiconcontent3 = scrapy.Field()
    subiconclass4 = scrapy.Field()
    subicontitle4 = scrapy.Field()
    subiconcontent4 = scrapy.Field()
    subiconclass5 = scrapy.Field()
    subicontitle5 = scrapy.Field()
    subiconcontent5 = scrapy.Field()
    shoptotalrate = scrapy.Field()
    shopdescscore = scrapy.Field()
    shopdescscorediff = scrapy.Field()
    shopdesccompare = scrapy.Field()
    shopdeliveryscore = scrapy.Field()
    shopdeliveryscorediff = scrapy.Field()
    shopdeliverycompare = scrapy.Field()
    shopservicescore = scrapy.Field()
    shopservicescorediff = scrapy.Field()
    shopservicecompare = scrapy.Field()
    product_price_float = scrapy.Field()
    product_sales_qty = scrapy.Field()
    shop_ave_score = scrapy.Field()


class ZhihuHotContent(scrapy.Item):
    hotid = scrapy.Field()
    partno = scrapy.Field()
    parttype = scrapy.Field()
    imgurl = scrapy.Field()
    imgnumber = scrapy.Field()
    videourl = scrapy.Field()
    text = scrapy.Field()
    

class ZhaoPinJobs(scrapy.Item):
    source = scrapy.Field()
    jobkey = scrapy.Field()
    jobid = scrapy.Field()
    jobtitle = scrapy.Field()
    salarystr = scrapy.Field()
    salary_month_min = scrapy.Field()
    salary_year_min = scrapy.Field()
    salary_month_max = scrapy.Field()
    salary_year_max = scrapy.Field()
    address = scrapy.Field()
    education = scrapy.Field()
    workexperience = scrapy.Field()
    release_time = scrapy.Field()
    response_time = scrapy.Field()
    companyname = scrapy.Field()
    industry = scrapy.Field()
    financing_situation = scrapy.Field()
    numberofpeople = scrapy.Field()
    welfare1 = scrapy.Field()
    welfare2 = scrapy.Field()
    welfare3 = scrapy.Field()
    welfare4 = scrapy.Field()
    welfare5 = scrapy.Field()