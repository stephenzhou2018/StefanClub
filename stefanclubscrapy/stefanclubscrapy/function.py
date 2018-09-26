from items import NbaNews,TaobaoProducts
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


def parse_taobao_products(auction,keyword,curr_num_of_img):
    taobao_product = TaobaoProducts()
    taobao_product["keyword"] = keyword
    taobao_product["product_id"] = auction['nid']
    imgsrcurl = auction['pic_url']
    imgsrcurl = get_utfurl_from_unicode(imgsrcurl)
    imgsrcurl = 'https:' + imgsrcurl
    imgsrcurl = imgsrcurl[:-1]
    file_name = "taobaoproduct_%s.jpg" % curr_num_of_img
    file_path = os.path.join("D:\StefanClub\StefanClub\www\static\img\\taobao", file_name)
    auto_download(imgsrcurl,file_path)
    taobao_product["imgsrcurl"] = "../static/img/taobao/%s" % file_name
    taobao_product["imgnumber"] = curr_num_of_img
    detail_url = auction['detail_url']
    detail_url = get_utfurl_from_unicode(detail_url)
    taobao_product["imgurl"] = detail_url
    samestyleurl = None
    similarurl = None
    if "i2iTags" in auction.keys():
        i2itags = auction['i2iTags']
        samestyle = i2itags['samestyle']
        samestyleurl = samestyle['url']
        samestyleurl = get_utfurl_from_unicode(samestyleurl)
        similar = i2itags['similar']
        similarurl = similar['url']
        similarurl = get_utfurl_from_unicode(similarurl)
    taobao_product["samestyleurl"] = samestyleurl
    taobao_product["similarurl"] = similarurl
    taobao_product["product_price"] = auction['view_price']
    taobao_product["payednum"] = auction['view_sales']
    title = auction['title']
    title = get_correct_title(title)
    taobao_product["title"] = title
    taobao_product["titleurl"] = detail_url
    taobao_product["shopname"] = auction['nick']
    shopLink = auction['shopLink']
    shopLink = get_utfurl_from_unicode(shopLink)
    taobao_product["shopurl"] = shopLink
    taobao_product["shopaddress"] = auction['item_loc']
    shopcard = auction['shopcard']
    levelclasses = shopcard['levelClasses']
    shopleveljingguanqty = 0
    shoplevelzuanqty = 0
    shoplevelguanqty = 0
    shoplevelxinqty = 0
    for levelclass in levelclasses:
        if levelclass['levelClass'] == 'icon-supple-level-jinguan':
            shopleveljingguanqty += 1
        elif levelclass['levelClass'] == 'icon-supple-level-guan':
            shoplevelguanqty += 1
        elif levelclass['levelClass'] == 'icon-supple-level-xin':
            shoplevelxinqty += 1
        elif levelclass['levelClass'] == 'icon-supple-level-zuan':
            shoplevelzuanqty += 1
        else:
            pass
    taobao_product["shoplevelzuanqty"] = shoplevelzuanqty
    taobao_product["shopleveljingguanqty"] = shopleveljingguanqty
    taobao_product["shoplevelguanqty"] = shoplevelguanqty
    taobao_product["shoplevelxinqty"] = shoplevelxinqty
    taobao_product["istmall"] = shopcard['isTmall']
    icons = auction['icon']
    for j in range(5):
        taobao_product["iconkey%s" % (j + 1)] = None
        taobao_product["icontitle%s" % (j + 1)] = None
        taobao_product["iconurl%s" % (j + 1)] = None
        taobao_product["subiconclass%s" % (j + 1)] = None
        taobao_product["subicontitle%s" % (j + 1)] = None
        taobao_product["subiconcontent%s" % (j + 1)] = None
    i = 1
    for icon in icons:
        taobao_product["iconkey%s" % i] = icon['icon_key']
        taobao_product["icontitle%s" % i] = icon['title']
        if "url" in icon.keys():
            taobao_product["iconurl%s" % i] = icon['url']
        if "iconPopupComplex" in icon.keys():
            iconpopupcomplex = icon['iconPopupComplex']
            taobao_product["subicontitle%s" % i] = iconpopupcomplex['popup_title']
            if "subIcons" in iconpopupcomplex.keys():
                subicons = iconpopupcomplex['subIcons']
                if len(subicons) > 0:
                    subicon = subicons[0]
                    taobao_product["subiconclass%s" % i] = subicon['dom_class']
                    taobao_product["subiconcontent%s" % i] = subicon['icon_content']
        if "iconPopupNormal" in icon.keys():
            iconpopupnormal = icon['iconPopupNormal']
            taobao_product["subiconclass%s" % i] = iconpopupnormal['dom_class']
        i += 1
    shoptotalrate = None
    if 'totalRate' in shopcard.keys():
        shoptotalrate = shopcard['totalRate']
        shoptotalrate = get_show_rate(shoptotalrate)
    taobao_product["shoptotalrate"] = shoptotalrate
    descriptions = shopcard['description']
    deliveries = shopcard['delivery']
    services = shopcard['service']
    taobao_product["shopdescscore"] = descriptions[0] / 100
    taobao_product["shopdescscorediff"] = descriptions[2] / 10000
    shopdesccompare = descriptions[1]
    if shopdesccompare > 0:
        shopdesccompare = 'higher'
    elif shopdesccompare < 0:
        shopdesccompare = 'lower'
    else:
        shopdesccompare = 'equal'
    taobao_product["shopdesccompare"] = shopdesccompare
    taobao_product["shopdeliveryscore"] = deliveries[0] / 100
    taobao_product["shopdeliveryscorediff"] = deliveries[2] / 10000
    shopdeliverycompare = deliveries[1]
    if shopdeliverycompare > 0:
        shopdeliverycompare = 'higher'
    elif shopdeliverycompare < 0:
        shopdeliverycompare = 'lower'
    else:
        shopdeliverycompare = 'equal'
    taobao_product["shopdeliverycompare"] = shopdeliverycompare
    taobao_product["shopservicescore"] = services[0] / 100
    taobao_product["shopservicescorediff"] = services[2] / 10000
    shopservicecompare = services[1]
    if shopservicecompare > 0:
        shopservicecompare = 'higher'
    elif shopservicecompare < 0:
        shopservicecompare = 'lower'
    else:
        shopservicecompare = 'equal'
    taobao_product["shopservicecompare"] = shopservicecompare
    return taobao_product


def get_zhihu_hotid(titleurl):
    titleurl_list = list(titleurl)
    max_index = -1
    for i in range(len(titleurl_list)):
        if titleurl_list[i] == '/':
            max_index = i
    hotid = titleurl[max_index + 1:]
    return hotid


def get_comment_qty(comment_title):
    comment_title_list = list(comment_title)
    max_index = -1
    for i in range(len(comment_title_list)):
        if comment_title_list[i] == '条':
            max_index = i
    comment_qty = comment_title[0:max_index]
    comment_qty = int(comment_qty)
    return comment_qty


def get_utfurl_from_unicode(url):
    url = url.encode('utf-8')
    url = str(url)
    url = url[2:]
    return url


def get_correct_title(ori_title):
    ori_title_list = list(ori_title)
    first_chi = -1
    for i in range(len(ori_title_list)):
        if u'\u4e00' <= ori_title_list[i] <= u'\u9fff':
            first_chi = i
            break
    eng_title = ori_title[:first_chi]
    chi_title = ori_title[first_chi-1:]
    correct_title = eng_title + chi_title
    return correct_title


def get_show_rate(ori_rate):
    ori_rate = str(ori_rate)
    ori_rate_list = list(ori_rate)
    ori_rate_len = len(ori_rate_list)
    if ori_rate_len == 4:
        ori_rate_list.insert(2, ".")
    elif ori_rate_len == 5:
        ori_rate_list.insert(3, ".")
    else:
        pass
    show_rate = "".join(ori_rate_list)
    show_rate = show_rate + '%'
    return show_rate


def auto_download(imgsrcurl,file_path):
    try:
        urllib.request.urlretrieve(imgsrcurl, file_path)
    except urllib.ContentTooShortError:
        print ('Network conditions is not good.Reloading.')
        auto_download(imgsrcurl,file_path)
