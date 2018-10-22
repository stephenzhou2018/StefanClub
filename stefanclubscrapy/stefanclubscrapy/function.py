from items import NbaNews,TaobaoProducts
from scrapy import Selector
import os,urllib,copy, requests
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
    if detail_url is not None:
        if detail_url[len(detail_url) - 1:] == "'":
            detail_url = detail_url[:-1]
    taobao_product["imgurl"] = detail_url
    samestyleurl = None
    similarurl = None
    if "i2iTags" in auction.keys():
        i2itags = auction['i2iTags']
        samestyle = i2itags['samestyle']
        samestyleurl = samestyle['url']
        samestyleurl = get_utfurl_from_unicode(samestyleurl)
        if samestyleurl == "'":
            samestyleurl = None
        if samestyleurl is not None:
            if samestyleurl[:22] == '/search?type=samestyle':
                samestyleurl = 'https://s.taobao.com' + samestyleurl
            if samestyleurl[len(samestyleurl) - 1:] == "'":
                samestyleurl = samestyleurl[:-1]
        similar = i2itags['similar']
        similarurl = similar['url']
        similarurl = get_utfurl_from_unicode(similarurl)
        if similarurl == "'":
            similarurl = None
        if similarurl is not None:
            if similarurl[:20] == '/search?type=similar':
                similarurl = 'https://s.taobao.com' + similarurl
            if similarurl[len(similarurl) - 1:] == "'":
                similarurl = similarurl[:-1]
    taobao_product["samestyleurl"] = samestyleurl
    taobao_product["similarurl"] = similarurl
    product_price = auction['view_price']
    product_price_float = float(product_price)
    taobao_product["product_price_float"] = product_price_float
    taobao_product["product_price"] = product_price
    payednum = None
    product_sales_qty = 0
    if 'view_sales' in auction.keys():
        payednum = auction['view_sales']
    if payednum is not None:
        product_sales_qty = payednum[:-3]
        product_sales_qty = int(product_sales_qty)
    taobao_product["product_sales_qty"] = product_sales_qty
    taobao_product["payednum"] = payednum
    orititle = auction['raw_title']
    title1,title2,new_title,titlehaskey = get_correct_title(orititle,keyword)
    taobao_product["title"] = new_title
    taobao_product["title1"] = title1
    taobao_product["title2"] = title2
    taobao_product["titlehaskey"] = titlehaskey
    taobao_product["titleurl"] = detail_url
    taobao_product["shopname"] = auction['nick']
    shopLink = auction['shopLink']
    shopLink = get_utfurl_from_unicode(shopLink)
    if shopLink is not None:
        if shopLink[len(shopLink) - 1:] == "'":
            shopLink = shopLink[:-1]
    taobao_product["shopurl"] = shopLink
    taobao_product["shopaddress"] = auction['item_loc']
    taobao_product["shoplevelzuanqty"] = 0
    taobao_product["shopleveljingguanqty"] = 0
    taobao_product["shoplevelguanqty"] = 0
    taobao_product["shoplevelxinqty"] = 0
    taobao_product["istmall"] = '0'
    taobao_product["shoptotalrate"] = None
    taobao_product["shopdescscore"] = None
    taobao_product["shopdescscorediff"] = None
    taobao_product["shopdesccompare"] = None
    taobao_product["shopdeliveryscore"] = None
    taobao_product["shopdeliveryscorediff"] = None
    taobao_product["shopdeliverycompare"] = None
    taobao_product["shopservicescore"] = None
    taobao_product["shopservicescorediff"] = None
    taobao_product["shopservicecompare"] = None
    taobao_product["shop_ave_score"] = 0
    shopdescscore = -1
    shopdeliveryscore = -1
    shopservicescore = -1
    if 'shopcard' in auction.keys():
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
        shoptotalrate = None
        if 'totalRate' in shopcard.keys():
            shoptotalrate = shopcard['totalRate']
            shoptotalrate = get_show_rate(shoptotalrate)
        taobao_product["shoptotalrate"] = shoptotalrate
        descriptions = shopcard['description']
        deliveries = shopcard['delivery']
        services = shopcard['service']
        if len(descriptions) > 0:
            shopdescscore = descriptions[0] / 100
            taobao_product["shopdescscore"] = shopdescscore
            shopdescscorediff = descriptions[2] / 100
            shopdescscorediff = str(shopdescscorediff) + '%'
            taobao_product["shopdescscorediff"] = shopdescscorediff
            shopdesccompare = descriptions[1]
            if shopdesccompare > 0:
                shopdesccompare = 'higher'
            elif shopdesccompare < 0:
                shopdesccompare = 'lower'
            else:
                shopdesccompare = 'equal'
            taobao_product["shopdesccompare"] = shopdesccompare
        if len(deliveries) > 0:
            shopdeliveryscore = deliveries[0] / 100
            taobao_product["shopdeliveryscore"] = shopdeliveryscore
            shopdeliveryscorediff = deliveries[2] / 100
            shopdeliveryscorediff = str(shopdeliveryscorediff) + '%'
            taobao_product["shopdeliveryscorediff"] = shopdeliveryscorediff
            shopdeliverycompare = deliveries[1]
            if shopdeliverycompare > 0:
                shopdeliverycompare = 'higher'
            elif shopdeliverycompare < 0:
                shopdeliverycompare = 'lower'
            else:
                shopdeliverycompare = 'equal'
            taobao_product["shopdeliverycompare"] = shopdeliverycompare
        if len(services) > 0:
            shopservicescore = services[0] / 100
            taobao_product["shopservicescore"] = shopservicescore
            shopservicescorediff = services[2] / 100
            shopservicescorediff = str(shopservicescorediff) + '%'
            taobao_product["shopservicescorediff"] = shopservicescorediff
            shopservicecompare = services[1]
            if shopservicecompare > 0:
                shopservicecompare = 'higher'
            elif shopservicecompare < 0:
                shopservicecompare = 'lower'
            else:
                shopservicecompare = 'equal'
            taobao_product["shopservicecompare"] = shopservicecompare
    if shopdescscore != -1 and shopdeliveryscore != -1 and shopservicescore != -1:
        taobao_product["shop_ave_score"] = (shopdescscore + shopdeliveryscore + shopservicescore) / 3

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
    if comment_qty == '添加评':
        return 0
    else:
        if comment_qty[-1:] == ' ':
            comment_qty = comment_qty[:-1]
        comment_qty  =  remove_comma(comment_qty)
        comment_qty = int(comment_qty)
        return comment_qty


def get_utfurl_from_unicode(url):
    url = url.encode('utf-8')
    url = str(url)
    url = url[2:]
    return url


def get_correct_title(ori_title,keyword):
    ori_title_list = list(ori_title)
    new_title = ''.join(ori_title_list)  # transfer the unicode to utf-8
    title1 = None
    title2 = None
    titlehaskey = 'FALSE'
    low_new_title = new_title.lower()
    low_key = keyword.lower()
    if low_key in low_new_title:
        titlehaskey = 'TRUE'
        keyword_index = low_new_title.index(low_key)
        keyword_len = len(keyword)
        title1 = new_title[:keyword_index]
        title2 = new_title[keyword_index + keyword_len:]
    return title1,title2,new_title,titlehaskey





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


def remove_comma(str):
    strlist = list(str)
    while ',' in strlist:
        for i in range(len(strlist)):
            if strlist[i] == ',':
                del strlist[i]
                break
    return ''.join(strlist)


def get_attribute(re_part_str,element):
    attributes = element.attrib
    for item in attributes.items():
        re_part_str = re_part_str + ' ' + item[0] + '=' + '"' + item[1] + '"'
    return re_part_str


def recursive(element):
    if element.tag == 'br':
        re_part_str = '<br/>'
        if element.tail is not None:
            re_part_str = re_part_str + element.tail
        return re_part_str
    elif element.tag == 'img':
        re_part_str = '<img'
        re_part_str = get_attribute(re_part_str,element)
        re_part_str = re_part_str + '>'
        if element.tail is not None:
            re_part_str = re_part_str + element.tail
        return re_part_str
    else:
        re_part_str = '<' + element.tag
        re_part_str = get_attribute(re_part_str, element)
        re_part_str = re_part_str + '>'
        if element.text is not None:
            re_part_str = re_part_str + element.text
        temp = element.getchildren()
        for j in range(len(temp)):
            re_part_str = re_part_str + recursive(temp[j])
        re_part_str = re_part_str + '</' + element.tag + '>'
        if element.tail is not None:
            re_part_str = re_part_str + element.tail
        return re_part_str


def get_real_videourl(video_id):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    }
    headers = {}
    headers['Referer'] = 'https://v.vzuu.com/video/{}'.format(video_id)
    headers['Origin'] = 'https://v.vzuu.com'
    headers['Host'] = 'lens.zhihu.com'
    headers['Content-Type'] = 'application/json'
    headers['Authorization'] = 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'

    api_video_url = 'https://lens.zhihu.com/api/videos/{}'.format(int(video_id))

    r = requests.get(api_video_url, headers={**HEADERS, **headers})
    # print(json.dumps(dict(r.request.headers), indent=2, ensure_ascii=False))
    # print(r.text.encode('utf-8').decode('unicode_escape'))
    playlist = r.json()['playlist']
    real_url = playlist['ld']['play_url']
    return real_url


def get_videourl(element):
    temp1 = element.getchildren()
    if len(temp1) < 2:
        real_videourl = None
        part_str = recursive(element)
    else:
        part_str = None
        content = temp1[1]
        temp2 = content.getchildren()
        if len(temp2) < 2:
            real_videourl = None
            part_str = recursive(element)
        else:
            url = temp2[1]
            temp3 = url.getchildren()
            if len(temp3) < 1:
                real_videourl = None
                part_str = recursive(element)
            else:
                video = temp3[0]
                surface_url = video.tail
                if surface_url is not None:
                    video_id = surface_url[28:]
                    real_videourl = get_real_videourl(video_id)
                    '''filename = '{}.mp4'.format(video_id)
                    opener = urllib.request.build_opener()
                    data = opener.open(real_videourl).read()
                    with open('D:\StefanClub\StefanClub\www\static\\video\zhihu\\' + filename, "wb") as code:
                        code.write(data)'''
                else:
                    real_videourl = None
                    part_str = recursive(element)
    return real_videourl, part_str


def get_img_info(element,curr_num_of_content, s, agentheaders):
    temp1 = element.getchildren()
    noscript = temp1[0]
    temp2 = noscript.getchildren()
    img = temp2[0]
    attributes = img.attrib
    items = attributes.items()
    for item in items:
        if item[0] == 'src':
            imgsrc = item[1]
            break
    file_name = "zhihuhotcontent_%s.jpg" % curr_num_of_content
    file_path = os.path.join("D:\StefanClub\StefanClub\www\static\img\zhihu", file_name)
    data = s.get(imgsrc, headers=agentheaders).content
    with open(file_path, "wb") as code:
        code.write(data)
    #urllib.request.urlretrieve(imgsrc, file_path)
    imgurl = "../static/img/zhihu/%s" % file_name
    return imgurl, curr_num_of_content
