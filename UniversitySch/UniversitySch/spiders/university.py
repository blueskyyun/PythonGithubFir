# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.downloadermiddlewares.retry import RetryMiddleware
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
import bs4
from UniversitySch.settings import user_agent_list
from UniversitySch.items import *
import traceback
import logging
from UniversitySch.ExceptionLog import *
import random
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
logfilename = genLogName()
nm = 'spiders' + logfilename
logging.basicConfig(filename=nm)


class UniversitySpider(scrapy.Spider):
    name = 'university'
    allowed_domains = ['baidu.com']
    url01 = 'https://baike.baidu.com/item/%E9%99%A2%E6%A0%A1%E4%BB%A3%E5%8F%B7/8106293?fr=aladdin#1'
    url02='http://www.zuihaodaxue.cn/zuihaodaxuepaiming2019.html'
    # https://college.zjut.cc/10545/dept/
    start_urls = ['https://baike.baidu.com/item/%E9%99%A2%E6%A0%A1%E4%BB%A3%E5%8F%B7/8106293?fr=aladdin#1']
    # 随机浏览器访问1
    headers = {
        'HOST': 'www.baidu.com',
        'Referer': 'http://www.baidu.com',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201',
        'Cookie': 'Y93u_f95e_saltkey = pc54M8pO;Y93u_f95e_lastvisit = 1561430143;Hm_lvt_70caf2c69029963059f939934ce83937 = 1561981850, 1562850835, 1562850874, 1562851035;Hm_lpvt_70caf2c69029963059f939934ce83937 = 1562897607'
    }
    headersSch = {
        'Referer': 'https://college.zjut.cc',
        'Cookie': 'Y93u_f95e_saltkey = pc54M8pO;Y93u_f95e_lastvisit = 1561430143;Hm_lvt_70caf2c69029963059f939934ce83937 = 1561981850, 1562850835, 1562850874, 1562851035;Hm_lpvt_70caf2c69029963059f939934ce83937 = 1562897607',
        'Host': 'college.zjut.cc',
        'Upgrade-Insecure-Requests': 1,
        'User-Agent': 'Mozilla/5.0(Windows NT 10.0; WOW64) AppleWebKit/537.36(KHTML, like Gecko) Chrome / 58.0 .3029.110 Safari / 537.36 SE 2.X MetaSr 1.0'
    }
    uname = ''
    count = 10
    def parse(self, response):
        body=response.text
        for item in Selector(text=body).css('table[log-set-param]'):
            loc = ''
            for item1 in item.css('tr'):
                if len(item1.css('b')) == 1:
                    location = item1.css('b::text').get()
                    loc = location[0:-2]
                else:
                    for item2 in item1.css('td[width]'):
                        codename = item2.css('::text').get()
                        if codename is not None:
                            codels = re.findall(r'\d+', codename)
                            namels = re.findall(r'[\u4e00-\u9fa5].*', codename)
                            if len(codels) > 0:
                                code = codels[0]
                                if len(namels) > 0:
                                    uname = namels[0]
                                else:
                                    uname = 'xxxx'
                                if loc == '' :
                                    loc = 'xxxx'
                                # item = UIDetailItem(unname=uname,code=code,location=loc)
                                # yield item
                                self.headersSch['User-Agent'] = random.choice(user_agent_list)
                                surl = 'http://college.zjut.cc/'+code+'/dept'
                                yield scrapy.Request(surl, headers=self.headersSch, callback=self.parse_us_bycode,dont_filter=True, meta={'uname':uname, 'code': code, 'loc': loc})

        # no = 0;
        # soup = BeautifulSoup(response.text, "html.parser")
        # # unvst = re.findall(r'\<div align=\"left\"\>', unvst)[0]
        # for tr in soup.find('tbody').children:
        #     no = no + 1
        #     if isinstance(tr, bs4.element.Tag):
        #         tds = tr('td')
        #         nname = tds[1].string
        #         # item = UItem(udic={'key':count, 'uname': nname})  #已载入数据库
        #         # item = UItem(uname = nname)
        #         keyword = nname + "院系"
        #         baiduUrl = u'http://www.baidu.com/baidu?wd=' + quote(keyword)
        #         # yield item
        #         # 对排名前200的大学在百度搜索学院--
        #         if no < 3:
        #             self.headers['User-Agent'] = random.choice(user_agent_list)
        #             yield scrapy.Request(baiduUrl, headers=self.headers, callback=self.parse_us, meta={'uname':nname, 'cnt':self.count})
    def parse_us(self, response):
        self.uname = response.meta['uname']
        self.count = response.meta['cnt']
        # tt = response.text
        # fd1 = open('us00.txt', 'w',encoding='utf-8')
        # fd1.write( tt)
        # fd1.close()
        body = response.text

        if self.count > 0:
            chrome_driver = 'D:\Program Files (x86)\chromedriver.exe'
            chrome_options = Options()
            # 设置chrome浏览器无界面模式
            chrome_options.add_argument('--headless')
            browser = webdriver.Chrome(options=chrome_options, executable_path=chrome_driver)
            for item in Selector(text=body).css('div.result.c-container'):
                try:
                    f13 = item.css('div.f13')
                    text = f13.get()
                    fd1 = open('us0.txt', 'w')
                    fd1.write( 'a\n')
                    fd1.close()
                    addr = f13.css('a:nth-child(1)::text').get()
                    ls = re.findall(r'edu\.cn/\s', addr)
                    if len(ls) == 1:
                        lb = item.css('h3.t')
                        href = lb.css('a::attr(href)').get()
                        nm  = lb.css('a').get()
                        # uName = re.findall(r'<em>[\u4e00-\u9fa5].*?</', nm)[0][4,-2]
                        # sName = re.findall(r'/em>[\u4e00-\u9fa5].*?<em', nm)[0][4, -3]
                        sname = re.findall(r'/em>[\u4e00-\u9fa5].*?<em', nm)
                        if len(sname)>0:
                            sName = sname[0][4:-3]
                            # self.headers['User-Agent'] = random.choice(user_agent_list)
                            # r = requests.get(href, allow_redirects=False, headers = self.headers)  # 禁止自动跳转
                            # if r.status_code == 302:
                            #     try:
                            #         realHref = r.headers['location']  # 返回指向的地址
                            #         href = realHref
                            #     except:
                            #         logging.error("********获取重定向地址失败***************************************************************")
                            #         pass
                            # fd = open('us2.txt', 'w')
                            # fd.write(sName+'\n')
                            # fd.close()
                            browser.get(href)
                            #             sleep(5)
                            # 打印页面网址
                            real_url = browser.current_url

                            item = USItem(uName = self.uname, sName = sName, href = real_url)
                            yield item
                except:
                    continue
             # 关闭浏览器
            browser.close()
            # 关闭chromedriver进程
            browser.quit()
            # nextPage = Selector(text=body).css('a.n')
            # isExist = True
            # if len(nextPage) == 1:
            #     np = nextPage[0]
            # elif len(nextPage) == 2:
            #     np = nextPage[1]
            # else:
            #     isExist = False
            # if isExist:
            #     nextPageUrl = np.css('a::attr(href)').extract()[0]
            for npage in Selector(text=body).css('a.n'):
                txt = npage.css('::text').get()
                ls = re.findall(r'下一页.*', txt)
                if len(ls) > 0:
                    nextPageUrl = npage.css('a::attr(href)').get()
                    nextUrl = 'http://www.baidu.com' + nextPageUrl
                    self.headers['User-Agent'] = random.choice(user_agent_list)
                    self.count = self.count - 1
                    yield scrapy.Request(nextUrl, headers=self.headers, callback=self.parse_us,meta={'uname':self.uname, 'cnt':self.count})
    def parse_us_bycode(self,response):

        if len(response.css('div.alert_error')) == 0:
            unameByPass = response.meta['uname']
            codeByPass = response.meta['code']
            locByPass = response.meta['loc']
            for item in response.css('p.col-sm-12.col-md-6 a'):
                school = item.css('::text').get()
                if school is not None:
                    if unameByPass=='xxxx':
                        if codeByPass == '10075' and locByPass == '河北省':
                            unameByPass = '河北大学'
                        elif codeByPass == '12605' and locByPass == '重庆市':
                            unameByPass = '重庆三峡职业学院'
                    if unameByPass != 'xxxx':
                        # usItem = UIDetailSchItem(udName=unameByPass, sdName=school)
                        # yield usItem
                        keyword = unameByPass+school
                        baiduUrl = u'http://www.baidu.com/baidu?wd=' + quote(keyword)
                        self.headers['User-Agent'] = random.choice(user_agent_list)
                        yield  scrapy.Request(baiduUrl, headers=self.headers,callback=self.parseSchHref, meta={'uName': unameByPass, 'code': codeByPass, 'school':school})

    def parseSchHref(self,response):
        uName = response.meta['uName']
        uCode = response.meta['code']
        schoolp = response.meta['school']

























