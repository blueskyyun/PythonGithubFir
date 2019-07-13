# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.downloadermiddlewares.retry import RetryMiddleware

from UniversitySch.items import *
from UniversitySch.DBUtil import *

logfilename = genLogName()
nm = 'pipelines' + logfilename
logging.basicConfig(filename=nm)


class UniversityschPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, UItem):
            dbutil1 = DBUtil()
            name = str(item['udic']['uname'])
            if name is not None:
                dbutil1.insertU(name)
        elif isinstance(item, USItem):
            dbutil2 = DBUtil()
            uName = str(item['uName'])
            sName = str(item['sName'])
            href = str(item['href'])
            # if uName != None and sName != None and href != None:
            print(uName+'-'+sName+'-'+href)
            dbutil2.inserUS(uName,sName,href)
        elif isinstance(item, UIDetailItem):
            dbutil3 = DBUtil()
            unname = str(item['unname'])
            code = str(item['code'])
            loc = str(item['location'])
            dbutil3.insert_unvstdetail3(unname,code,loc)
        elif isinstance(item, UIDetailSchItem):
            dbutil4 = DBUtil()
            uname = str(item['udName'])
            sname = str(item['sdName'])
            dbutil4.inserUdetail1S(uname,sname)






class UniversityInfoPipeline(object):

    # 当一个爬虫被调用时，pipeline启动的方法
    def open_spider(self, spider):
        self.f = open('u.txt', 'w')
    # 一个爬虫关闭或结束时，pipeline对应的方法
    def close_spider(self, spider):
        self.f.close()
    def process_item(self, item, spider):

        if isinstance(item, USItem):

            try:
                # key = item['udic']
                line = str(item['sName']) + '\n'    #不用str解析不出来
        # line = str(item['dict']) + 'a'+'\n'
                self.f.write(line)
            except:
                pass
        return item    #希望有其他函数可以处理这个item，我们就返回这个item

