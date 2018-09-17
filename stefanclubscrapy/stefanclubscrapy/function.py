from items import NbaNews
from scrapy import Selector
import os,urllib,copy
from pipelines import get_max_num


def parse_lefttop(lefttopimg_node):
    max_lefttop_num = get_max_num('lefttop')
    if max_lefttop_num is None:
        max_lefttop_num = 0
    curr_num_of_letop = max_lefttop_num + 1
    nbanews = NbaNews()
    lefttopsel = Selector(text=str(lefttopimg_node), type="html", )
    lefttoptitle = lefttopsel.xpath('//h3/text()').extract()[0].strip()
    lefttopurl = lefttopsel.xpath('//a//@href').extract()[0].strip()
    lefttopimgsrcurl = lefttopsel.xpath('//img//@src').extract()[0].strip()
    lefttopisvideo = lefttopurl[2:7]
    if lefttopisvideo == 'video':
        lefttopisvideo = 'TRUE'
    else:
        lefttopisvideo = 'FALSE'
    lefttopfile_name = "lefttop_%s.jpg" % curr_num_of_letop
    lefttopfile_path = os.path.join("D:\StefanClub\StefanClub\www\static\img\sinasports", lefttopfile_name)
    urllib.request.urlretrieve(lefttopimgsrcurl, lefttopfile_path)
    nbanews["number"] = curr_num_of_letop
    #curr_num_of_letop = curr_num_of_letop + 1
    nbanews["imgsrcurl"] = "../static/img/sinasports/%s" % lefttopfile_name
    nbanews["imgurl"] = lefttopurl
    nbanews["isvideo"] = lefttopisvideo
    nbanews["title"] = lefttoptitle
    nbanews["titleurl"] = None
    nbanews["newstime"] = None
    nbanews["comment_url"] = None
    for j in range(1, 6):
        nbanews["tag%s" % j] = None
        nbanews["tag%surl" % j] = None
    nbanews["newstype"] = 'lefttop'
    return nbanews


def parse_lefttoplines(lefttoplines):
    nbanews = NbaNews()
    nbanewslist = [None] * len(lefttoplines)
    i = 0
    for lefttopline in lefttoplines:
        sel = Selector(text=str(lefttopline), type="html", )
        title = sel.xpath('//a/text()').extract()[0].strip()
        titleurl = sel.xpath('//a//@href').extract()[0].strip()
        nbanews["number"] = None
        nbanews["imgsrcurl"] = None
        nbanews["imgurl"] = None
        nbanews["isvideo"] = None
        nbanews["title"] = title
        nbanews["titleurl"] = titleurl
        nbanews["newstime"] = None
        nbanews["comment_url"] = None
        for j in range(1, 6):
            nbanews["tag%s" % j] = None
            nbanews["tag%surl" % j] = None
        nbanews["newstype"] = 'lefttoplines'
        nbanewslist[i] = copy.deepcopy(nbanews)
        i += 1
    return nbanewslist


def parse_leftsecond(leftsecond_node):
    max_leftsec_num = get_max_num('leftsec')
    if max_leftsec_num is None:
        max_leftsec_num = 0
    curr_num_of_lesec = max_leftsec_num + 1
    nbanews = NbaNews()
    leftsecsel = Selector(text=str(leftsecond_node), type="html", )
    leftsecimgsrcurl = leftsecsel.xpath('//img//@src').extract()[0].strip()

    leftsecfile_name = "leftsec_%s.jpg" % curr_num_of_lesec
    leftsecfile_path = os.path.join("D:\StefanClub\StefanClub\www\static\img\sinasports", leftsecfile_name)
    urllib.request.urlretrieve(leftsecimgsrcurl, leftsecfile_path)
    nbanews["number"] = curr_num_of_lesec
    #curr_num_of_lesec = curr_num_of_lesec + 1
    nbanews["imgsrcurl"] = "../static/img/sinasports/%s" % leftsecfile_name
    nbanews["imgurl"] = None
    nbanews["isvideo"] = None
    nbanews["title"] = None
    nbanews["titleurl"] = None
    nbanews["newstime"] = None
    nbanews["comment_url"] = None
    for j in range(1, 6):
        nbanews["tag%s" % j] = None
        nbanews["tag%surl" % j] = None
    nbanews["newstype"] = 'leftsec'
    return nbanews


def parse_leftsectxt(leftsecond_node):
    nbanews = NbaNews()
    leftsecsel = Selector(text=str(leftsecond_node), type="html", )
    leftsectxts = leftsecsel.xpath('//a')
    leftsectxtlen = len(leftsectxts)
    if leftsectxtlen > 0:
        titles = [''] * leftsectxtlen
        urls = [''] * leftsectxtlen
        nbanewslist = [ None] * leftsectxtlen
        for i in range(leftsectxtlen):
            titles[i] = leftsecsel.xpath('//a/text()').extract()[i].strip()
            urls[i] = leftsecsel.xpath('//a//@href').extract()[i].strip()
            nbanews["number"] = None
            nbanews["imgsrcurl"] = None
            nbanews["imgurl"] = None
            nbanews["isvideo"] = None
            nbanews["title"] = titles[i]
            nbanews["titleurl"] = urls[i]
            nbanews["newstime"] = None
            nbanews["comment_url"] = None
            for jj in range(1, 6):
                nbanews["tag%s" % jj] = None
                nbanews["tag%surl" % jj] = None
            nbanews["newstype"] = 'leftsectxt'
            nbanewslist[i] = copy.deepcopy(nbanews)
        return nbanewslist
    return None


def get_zhihu_hotid(titleurl):
    titleurl_list = list(titleurl)
    max_index = -1
    for i in range(len(titleurl_list)):
        if titleurl_list[i] == '/':
            max_index = i
    hotid = titleurl[max_index + 1:]
    return hotid
