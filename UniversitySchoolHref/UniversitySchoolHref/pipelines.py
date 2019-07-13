# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from UniversitySchoolHref.items import *
from UniversitySchoolHref.DBUtil import *

class UniversityschoolhrefPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,SchoolHrefItem):
            pusid = str(item['usid'])
            phref = str(item['href'])
            dbUtil1 = DBUtil()
            dbUtil1.updateSchHref(pusid,phref)
        # return item
