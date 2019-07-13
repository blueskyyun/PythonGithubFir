# -*- coding: utf-8 -*-
import scrapy
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from UniversitySchoolHref.items import *
from UniversitySchoolHref.DBUtil import *
from urllib.parse import quote
import random
from UniversitySchoolHref.settings import *
chrome_driver = 'D:\Program Files (x86)\chromedriver.exe'

# browser.set_page_load_timeout(10)
count =13459
class HrefSpider(scrapy.Spider):
    name = 'href'
    allowed_domains = ['baidu.com']
    start_urls = ['https://www.baidu.com/s?wd=%E5%8C%97%E4%BA%AC%E5%A4%A7%E5%AD%A6%E6%95%B0%E5%AD%A6%E7%A7%91%E5%AD%A6%E5%AD%A6%E9%99%A2']
    headers = {
        'HOST': 'www.baidu.com',
        'Referer': 'http://www.baidu.com',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201'
    }


    def parse(self, response):
        isFind = False
        for item in response.css('div.result.c-container'):
            fd1 = open('us00.txt', 'w', encoding='utf-8')
            fd1.write(item.get())
            fd1.close()
            try:
                f13 = item.css('div.f13')
                if len(f13) > 0:
                    addr = f13.css('a:nth-child(1)::text').get()
                    if addr is not None:
                        ls = re.findall(r'edu\.cn', addr)
                        if len(ls) > 0:
                            lb = item.css('h3.t')
                            em = lb.css('em::text').getall()
                            for e in em:
                                schmp = re.findall(r'数学科学学院',e)
                                if len(schmp) > 0:
                                    isFind = True
                                    href = lb.css('a::attr(href)').get()
                                    # 开始请求
                                    try:
                                        chrome_options = Options()
                                        # 设置chrome浏览器无界面模式
                                        chrome_options.add_argument('--headless')
                                        browser = webdriver.Chrome(options=chrome_options,
                                                                   executable_path=chrome_driver)
                                        browser.get(href)
                                        sleep(1)
                                        realUrl = browser.current_url
                                        browser.close()
                                        browser.quit()
                                    except:
                                        isFind=False
                                        break
                                    if realUrl is not None:
                                        hItem = SchoolHrefItem(usid=1,href=realUrl)
                                        yield hItem
                                        break

                                elif len(e) > 5:
                                    isFind = True
                                    href = lb.css('a::attr(href)').get()
                                try:
                                    chrome_options = Options()
                                    # 设置chrome浏览器无界面模式
                                    chrome_options.add_argument('--headless')
                                    browser = webdriver.Chrome(options=chrome_options,
                                                               executable_path=chrome_driver)
                                    browser.get(href)
                                    sleep(1)
                                    realUrl = browser.current_url
                                    browser.close()
                                    browser.quit()
                                except:
                                    isFind=False
                                    break
                                if realUrl is not None:
                                    hItem = SchoolHrefItem(usid=1, href=realUrl)
                                    yield hItem
                                    break

            except:
                continue

        dbUtil0 = DBUtil()
        data = dbUtil0.selectByUsid(2)
        if data is not None:
            unid = data[1]
            school = data[2]
            uname = dbUtil0.select_unvstdetail3(unid)
            if uname is not None:
                keyword = uname[0]+school
                baiduUrl = u'http://www.baidu.com/baidu?wd=' + quote(keyword)
                self.headers['User-Agent'] = random.choice(user_agent_list)
                yield scrapy.Request(baiduUrl,callback=self.parse_school,meta={'school':school,'no': 2})
    def parse_school(self,response):
        isFind=False
        sch_name = response.meta['school']
        no = response.meta['no']
        for item in response.css('div.result.c-container'):
            try:
                f13 = item.css('div.f13')
                if len(f13) > 0:
                    addr = f13.css('a:nth-child(1)::text').get()
                    if addr is not None:
                        ls = re.findall(r'edu\.cn', addr)
                        if len(ls) > 0:
                            lb = item.css('h3.t')
                            em = lb.css('em::text').getall()
                            for e in em:
                                schmp = re.findall(sch_name,e)
                                if len(schmp) > 0:
                                    isFind=True
                                    href = lb.css('a::attr(href)').get()
                                    try:
                                        chrome_options = Options()
                                        # 设置chrome浏览器无界面模式
                                        chrome_options.add_argument('--headless')
                                        browser = webdriver.Chrome(options=chrome_options,
                                                                   executable_path=chrome_driver)
                                        # 开始请求
                                        browser.get(href)
                                        sleep(1)
                                        realUrl = browser.current_url
                                        browser.close()
                                        browser.quit()
                                    except:
                                        break
                                    if realUrl is not None:
                                        hItem = SchoolHrefItem(usid=no,href=realUrl)
                                        yield hItem
                                        break
                                elif len(e) > 5:
                                    href = lb.css('a::attr(href)').get()
                                    try:
                                        chrome_options = Options()
                                        # 设置chrome浏览器无界面模式
                                        chrome_options.add_argument('--headless')
                                        browser = webdriver.Chrome(options=chrome_options,
                                                                   executable_path=chrome_driver)
                                        browser.get(href)
                                        sleep(1)
                                        realUrl = browser.current_url
                                        browser.close()
                                        browser.quit()
                                    except:
                                        break
                                    if realUrl is not None:
                                        hItem = SchoolHrefItem(usid=no, href=realUrl)
                                        yield hItem
                                        break
            except:
                continue
        # browser.close()
        if no < count:
            no = no +1
            dbUtil0 = DBUtil()
            data = dbUtil0.selectByUsid(no)
            if data is not None:
                unid = data[1]
                school = data[2]
                uname = dbUtil0.select_unvstdetail3(unid)
                if uname is not None:
                    keyword = uname[0]+school
                    baiduUrl = u'http://www.baidu.com/baidu?wd=' + quote(keyword)
                    self.headers['User-Agent'] = random.choice(user_agent_list)
                    yield scrapy.Request(baiduUrl,callback=self.parse_school,meta={'school':school,'no':no})


