# -*- coding: utf-8 -*-
import scrapy,json,os,urllib,datetime
from scrapy import Request,Selector
from items import HotMatches,SinaCarousel,HotMatchNews,NbaNews
from bs4 import BeautifulSoup
from pipelines import get_max_num
from function import parse_lefttop,parse_leftsecond,parse_leftsectxt,parse_lefttoplines


class SinasportsSpider(scrapy.Spider):
    name = 'sinasports'
    allowed_domains = ['sports.sina.com.cn']
    start_urls = ['http://sports.sina.com.cn/']

    matcher_api_url = 'http://sports.sina.com.cn/iframe/js/2015/live.js?dpc=1'
    nbanews_url = '''http://cre.mix.sina.com.cn/get/cms/feed?callback=jQuery111304795819583663854_1535281251386
                  &pcProduct=31&ctime=&merge=3&mod=pcsptw&cre=tianyi&statics=1
                  &length=12&ad=%7B%22rotate_count%22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22
                  tianyi_pcspt%22%2C%22page_url%22%3A%22http%3A%2F%2Fsports.sina.com.cn%2F%22%2C%22
                  timestamp%22%3A1535281251422+%7D&_=1535281251395]'''
    intsoc_url = '''http://cre.mix.sina.com.cn/get/cms/feed?callback=jQuery111306164420163923745_1535782658772
                &pcProduct=30&ctime=&merge=3&mod=pcsptw&cre=tianyi&statics=1&length=12&ad=%7B%22rotate_count
                %22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pcspt%22%2C%22page_url%22
                %3A%22http%3A%2F%2Fsports.sina.com.cn%2F%22%2C%22timestamp%22%3A1535782658814+%7D&_=1535782658971'''
    chisoc_url = '''http://cre.mix.sina.com.cn/get/cms/feed?callback=jQuery111306164420163923745_1535782658772
                 &pcProduct=29&ctime=&merge=3&mod=pcsptw&cre=tianyi&statics=1&length=12&ad=%7B%22rotate_count
                 %22%3A100%2C%22platform%22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pcspt%22%2C%22page_url%22%3A
                 %22http%3A%2F%2Fsports.sina.com.cn%2F%22%2C%22timestamp%22%3A1535782658814+%7D&_=1535782659005'''
    cba_url = '''http://cre.mix.sina.com.cn/get/cms/feed?callback=jQuery111306164420163923745_1535782658772&pcProduct=32
               &ctime=&merge=3&mod=pcsptw&cre=tianyi&statics=1&length=12&ad=%7B%22rotate_count%22%3A100%2C%22platform
               %22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pcspt%22%2C%22page_url%22%3A%22http%3A%2F%2Fsports.sina.com.cn
               %2F%22%2C%22timestamp%22%3A1535782658814+%7D&_=1535782659010'''
    sum_url = '''http://cre.mix.sina.com.cn/get/cms/feed?callback=jQuery111306164420163923745_1535782658772&pcProduct=33
               &ctime=&merge=3&mod=pcsptw&cre=tianyi&statics=1&length=12&ad=%7B%22rotate_count%22%3A100%2C%22platform
               %22%3A%22pc%22%2C%22channel%22%3A%22tianyi_pcspt%22%2C%22page_url%22%3A%22http%3A%2F%2Fsports.sina.com.cn
               %2F%22%2C%22timestamp%22%3A1535782658814+%7D&_=1535782659015'''

    max_car_number = get_max_num('sinacar')
    if max_car_number is None:
        max_car_number = 0
    curr_num_of_car = max_car_number + 1

    max_hotmatnews_num = get_max_num('hotmatch_news')
    if max_hotmatnews_num is None:
        max_hotmatnews_num = 0
    curr_num_of_hmn = max_hotmatnews_num + 1

    max_nbanews_num = get_max_num('nbanews')
    if max_nbanews_num is None:
        max_nbanews_num = 0
    curr_num_of_nba = max_nbanews_num + 1

    max_lefttop_num = get_max_num('lefttop')
    if max_lefttop_num is None:
        max_lefttop_num = 0
    curr_num_of_letop = max_lefttop_num + 1

    max_leftsec_num = get_max_num('leftsec')
    if max_leftsec_num is None:
        max_leftsec_num = 0
    curr_num_of_lesec = max_leftsec_num + 1

    def start_requests(self):
        yield Request(self.nbanews_url, meta={"newstype":"NBA","request_url":self.nbanews_url}, callback=self.parse_nba_news)
        yield Request(self.intsoc_url, meta={"newstype":"INTSOC","request_url":self.intsoc_url}, callback=self.parse_nba_news)
        yield Request(self.chisoc_url, meta={"newstype":"CHISOC","request_url":self.chisoc_url}, callback=self.parse_nba_news)
        yield Request(self.cba_url, meta={"newstype":"CBA","request_url":self.cba_url}, callback=self.parse_nba_news)
        yield Request(self.sum_url, meta={"newstype":"SUM","request_url":self.sum_url}, callback=self.parse_nba_news)
        for start_url in self.start_urls:
            yield Request(start_url,callback=self.parse_main)
        yield Request(self.matcher_api_url, callback=self.parse_matches)

    def parse_matches(self, response):
        hotmatches = HotMatches()
        html = response.text
        html = html[:-13]
        html = html[42:]
        resultjson = json.loads(html)
        matches = resultjson['matches']
        for match in matches:
            livecast_id = match['livecast_id']
            shorttitle = match['ShortTitle']
            round_cn = match['Round_cn']
            title = shorttitle + round_cn
            team1 =  match['Team1']
            team2 =  match['Team2']
            score1 = match['Score1']
            score2 = match['Score2']
            if not score1.strip() and not score2.strip():
                matchtype = 'pre'
            else:
                matchtype = 'post'
            matchdate =  match['date']
            matchdate = matchdate[5:]
            matchtime =  match['time']
            newsurl =  match['NewsUrl']
            liveurl =  match['LiveUrl']
            match_url =  match['match_url']

            hotmatches['livecast_id'] = livecast_id
            hotmatches['type'] = matchtype
            hotmatches['title'] = title
            hotmatches['team1'] = team1
            hotmatches['team2'] = team2
            hotmatches['score1'] = score1
            hotmatches['score2'] = score2
            hotmatches['matchdate'] = matchdate
            hotmatches['matchtime'] = matchtime
            hotmatches['newsurl'] = newsurl
            hotmatches['liveurl'] = liveurl
            hotmatches['match_url'] = match_url

            if hotmatches['team1'] and hotmatches['team2']:
                yield hotmatches

    def parse_main(self, response):
        sinacarousel = SinaCarousel()
        hotmatchnews = HotMatchNews()
        nbanews = NbaNews()
        lefttop_nbanews = NbaNews()
        leftsec_nbanews = NbaNews()
        leftsectxt_nbanewslist = []
        soup = BeautifulSoup(response.text, 'lxml')
        post_nodes = soup.select("ul[class='slide-focus-d-cont'] li[class='clearfix thumbnail-b-gra']")
        post_nodes1 = soup.select("div[node-type='tytopwrap']")
        lefttopimg_node = soup.select("div[data-sudaclick='blk_focusvideo'] div[class='thumbnail-b thumbnail-b-gra thumbnail-b-video']")[0]
        post_nodes2 = soup.select("div[data-sudaclick='blk_focusvideo'] div[class='layout-mt-g news-list-e'] p")
        leftsecond_node = soup.select("div[class='layout-mt-h layout-mb-e news-hot']")[0]

        lefttop_nbanews = parse_lefttop(lefttopimg_node)
        yield lefttop_nbanews
        lefttoplines_nbanewslist = parse_lefttoplines(post_nodes2)
        for i in range(0,len(lefttoplines_nbanewslist)):
            if lefttoplines_nbanewslist[i] is not None:
                yield lefttoplines_nbanewslist[i]
        leftsec_nbanews =  parse_leftsecond(leftsecond_node)
        yield leftsec_nbanews
        leftsectxt_nbanewslist = parse_leftsectxt(leftsecond_node)
        for i in range(0,len(leftsectxt_nbanewslist)):
            yield leftsectxt_nbanewslist[i]

        for post_node in post_nodes:
            sel = Selector(text=str(post_node), type="html", )
            title = sel.xpath('//p/text()').extract()[0].strip()
            url = sel.xpath('//a//@href').extract()[0].strip()
            img_url = sel.xpath('//img//@src').extract()[0].strip()
            file_name = "carousel_%s.jpg" % self.curr_num_of_car
            file_path = os.path.join("D:\StefanClub\StefanClub\www\static\img\sinasports", file_name)
            urllib.request.urlretrieve(img_url, file_path)

            sinacarousel["number"] = self.curr_num_of_car
            self.curr_num_of_car = self.curr_num_of_car + 1
            sinacarousel["title"] = title
            sinacarousel["url"] = url
            #carousel_item["img_url"] = img_url
            sinacarousel["img_url"] = "../static/img/sinasports/%s" % file_name
            yield sinacarousel

        for post_node1 in post_nodes1:
            sel1 = Selector(text=str(post_node1), type="html", )
            titles = sel1.xpath('//h3/a')
            title1 = ''
            title2 = ''
            title3 = ''
            title1url = ''
            title2url = ''
            title3url = ''
            if len(titles) == 3:
                title1 = sel1.xpath('//h3/a/text()').extract()[0].strip()
                title2 = sel1.xpath('//h3/a/text()').extract()[1].strip()
                title3 = sel1.xpath('//h3/a/text()').extract()[2].strip()
                title1url = sel1.xpath('//h3/a//@href').extract()[0].strip()
                title2url = sel1.xpath('//h3/a//@href').extract()[1].strip()
                title3url = sel1.xpath('//h3/a//@href').extract()[2].strip()
            elif len(titles) == 2:
                title1 = sel1.xpath('//h3/a/text()').extract()[0].strip()
                title2 = sel1.xpath('//h3/a/text()').extract()[1].strip()
                title3 = ''
                title1url = sel1.xpath('//h3/a//@href').extract()[0].strip()
                title2url = sel1.xpath('//h3/a//@href').extract()[1].strip()
                title3url = ''
            elif len(titles) == 1:
                title1 = sel1.xpath('//h3/a/text()').extract()[0].strip()
                title2 = ''
                title3 = ''
                title1url = sel1.xpath('//h3/a//@href').extract()[0].strip()
                title2url = ''
                title3url = ''
            else:
                pass
            imgurl = sel1.xpath('//div[@class="ty-card-thumb-w"]/a//@href').extract()[0].strip()
            imgsrcurl = sel1.xpath('//img//@src').extract()[0].strip()
            imgsrcurl = 'http:' + imgsrcurl
            file_name1 = "hotmatchnews_%s.jpg" % self.curr_num_of_hmn
            file_path1 = os.path.join("D:\StefanClub\StefanClub\www\static\img\sinasports", file_name1)
            urllib.request.urlretrieve(imgsrcurl, file_path1)

            li1 = sel1.xpath('//li').extract()[0].strip()
            li2 = sel1.xpath('//li').extract()[1].strip()
            li3 = sel1.xpath('//li').extract()[2].strip()
            subsel1 = Selector(text=str(li1), type="html", )
            subsel2 = Selector(text=str(li2), type="html", )
            subsel3 = Selector(text=str(li3), type="html", )
            lia1 = subsel1.xpath('//a')
            lia2 = subsel2.xpath('//a')
            lia3 = subsel3.xpath('//a')
            line1 = ''
            line2 = ''
            line3 = ''
            line4 = ''
            line5 = ''
            line6 = ''
            line7 = ''
            line8 = ''
            line9 = ''
            line1url = ''
            line2url = ''
            line3url = ''
            line4url = ''
            line5url = ''
            line6url = ''
            line7url = ''
            line8url = ''
            line9url = ''
            if len(lia1) == 3:
                line1 = subsel1.xpath('//a/text()').extract()[0].strip()
                line2 = subsel1.xpath('//a/text()').extract()[1].strip()
                line3 = subsel1.xpath('//a/text()').extract()[2].strip()
                line1url = subsel1.xpath('//a//@href').extract()[0].strip()
                line2url = subsel1.xpath('//a//@href').extract()[1].strip()
                line3url = subsel1.xpath('//a//@href').extract()[2].strip()
            elif len(lia1) == 2:
                line1 = subsel1.xpath('//a/text()').extract()[0].strip()
                line2 = subsel1.xpath('//a/text()').extract()[1].strip()
                line3 = ''
                line1url = subsel1.xpath('//a//@href').extract()[0].strip()
                line2url = subsel1.xpath('//a//@href').extract()[1].strip()
                line3url = ''
            elif len(lia1) == 1:
                line1 = subsel1.xpath('//a/text()').extract()[0].strip()
                line2 = ''
                line3 = ''
                line1url = subsel1.xpath('//a//@href').extract()[0].strip()
                line2url = ''
                line3url = ''
            else:
                pass

            if len(lia2) == 3:
                line4 = subsel2.xpath('//a/text()').extract()[0].strip()
                line5 = subsel2.xpath('//a/text()').extract()[1].strip()
                line6 = subsel2.xpath('//a/text()').extract()[2].strip()
                line4url = subsel2.xpath('//a//@href').extract()[0].strip()
                line5url = subsel2.xpath('//a//@href').extract()[1].strip()
                line6url = subsel2.xpath('//a//@href').extract()[2].strip()
            elif len(lia2) == 2:
                line4 = subsel2.xpath('//a/text()').extract()[0].strip()
                line5 = subsel2.xpath('//a/text()').extract()[1].strip()
                line6 = ''
                line4url = subsel2.xpath('//a//@href').extract()[0].strip()
                line5url = subsel2.xpath('//a//@href').extract()[1].strip()
                line6url = ''
            elif len(lia2) == 1:
                line4 = subsel2.xpath('//a/text()').extract()[0].strip()
                line5 = ''
                line6 = ''
                line4url = subsel2.xpath('//a//@href').extract()[0].strip()
                line5url = ''
                line6url = ''
            else:
                pass

            if len(lia3) == 3:
                line7 = subsel3.xpath('//a/text()').extract()[0].strip()
                line8 = subsel3.xpath('//a/text()').extract()[1].strip()
                line9 = subsel3.xpath('//a/text()').extract()[2].strip()
                line7url = subsel3.xpath('//a//@href').extract()[0].strip()
                line8url = subsel3.xpath('//a//@href').extract()[1].strip()
                line9url = subsel3.xpath('//a//@href').extract()[2].strip()
            elif len(lia3) == 2:
                line7 = subsel3.xpath('//a/text()').extract()[0].strip()
                line8 = subsel3.xpath('//a/text()').extract()[1].strip()
                line9 = ''
                line7url = subsel3.xpath('//a//@href').extract()[0].strip()
                line8url = subsel3.xpath('//a//@href').extract()[1].strip()
                line9url = ''
            elif len(lia3) == 1:
                line7 = subsel3.xpath('//a/text()').extract()[0].strip()
                line8 = ''
                line9 = ''
                line7url = subsel3.xpath('//a//@href').extract()[0].strip()
                line8url = ''
                line9url = ''
            else:
                pass

            hotmatchnews["number"] = self.curr_num_of_hmn
            self.curr_num_of_hmn = self.curr_num_of_hmn + 1
            hotmatchnews["title1"] = title1
            hotmatchnews["title2"] = title2
            hotmatchnews["title3"] = title3
            hotmatchnews["title1url"] = title1url
            hotmatchnews["title2url"] = title2url
            hotmatchnews["title3url"] = title3url
            hotmatchnews["imgsrcurl"] = "../static/img/sinasports/%s" % file_name1
            hotmatchnews["imgurl"] = imgurl
            hotmatchnews["line1"] = line1
            hotmatchnews["line2"] = line2
            hotmatchnews["line3"] = line3
            hotmatchnews["line1url"] = line1url
            hotmatchnews["line2url"] = line2url
            hotmatchnews["line3url"] = line3url
            hotmatchnews["line4"] = line4
            hotmatchnews["line5"] = line5
            hotmatchnews["line6"] = line6
            hotmatchnews["line4url"] = line4url
            hotmatchnews["line5url"] = line5url
            hotmatchnews["line6url"] = line6url
            hotmatchnews["line7"] = line7
            hotmatchnews["line8"] = line8
            hotmatchnews["line9"] = line9
            hotmatchnews["line7url"] = line7url
            hotmatchnews["line8url"] = line8url
            hotmatchnews["line9url"] = line9url

            yield hotmatchnews




    def parse_nba_news(self, response):
        nbanews = NbaNews()
        newstype = response.meta.get("newstype", "")
        request_url = response.meta.get("request_url", "")
        html = response.text
        if html[0:6] == 'jQuery':
            html = html[:-3]
            html = html[43:]
        prejson = json.loads(html)
        if "data" in prejson.keys():
            nbanewslist = prejson['data']
            for nbanewsitem in nbanewslist:
                imgsrcurl = nbanewsitem["thumb"]
                imgurl = ''
                isvideo = 'FALSE'
                file_name = ''
                nbanews["number"] = -1
                if imgsrcurl:
                    imgurl = nbanewsitem["url"]
                    if imgurl is None:
                        imgurl = nbanewsitem["url_https"]
                    #if nbanewsitem.has_key('video_id'):
                    if "video_id" in nbanewsitem.keys():
                        video_id = nbanewsitem["video_id"]
                        if video_id is not None:
                            isvideo = 'TRUE'
                    file_name = "nbanews_%s.jpg" % self.curr_num_of_nba
                    file_path = os.path.join("D:\StefanClub\StefanClub\www\static\img\sinasports", file_name)
                    urllib.request.urlretrieve(imgsrcurl, file_path)

                    nbanews["number"] = self.curr_num_of_nba
                    self.curr_num_of_nba = self.curr_num_of_nba + 1

                title = nbanewsitem["title"]
                titleurl =  nbanewsitem["url"]
                if titleurl is None:
                    titleurl = nbanewsitem["url_https"]
                newstime = nbanewsitem["mtime"]
                newstime = datetime.datetime.fromtimestamp(newstime)
                comment_id = nbanewsitem["new_commentid"]
                channnel  = comment_id[0:2]
                newsid = comment_id[3:-2]
                comment_url = "http://comment5.news.sina.com.cn/comment/skin/default.html?channel=" + channnel + "&amp;newsid=" + newsid
                labels = nbanewsitem["labels"]
                labellist = [''] * 5
                if isinstance(labels, dict):
                    i = 0
                    for key in labels.keys():
                        labellist[i] = key
                        i += 1

                nbanews["imgsrcurl"] = "../static/img/sinasports/%s" % file_name
                nbanews["imgurl"] = imgurl
                nbanews["isvideo"] = isvideo
                nbanews["title"] = title
                nbanews["titleurl"] = titleurl
                nbanews["newstime"] = newstime
                nbanews["comment_url"] = comment_url
                jj = 1
                for j in labellist:
                    nbanews["tag%s" % jj] = j
                    nbanews["tag%surl" % jj] = "//tags.sports.sina.com.cn/" + j
                    jj += 1
                nbanews["newstype"] = newstype
                yield nbanews
        else:
             yield Request(request_url, meta={"newstype": newstype, "request_url": request_url},callback=self.parse_nba_news)

