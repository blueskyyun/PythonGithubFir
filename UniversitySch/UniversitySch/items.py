# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.downloadermiddlewares.retry import RetryMiddleware


class UniversityschItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class UItem(scrapy.Item):
    udic = scrapy.Field()
    # uname = ""

class USItem(scrapy.Item):
    uName = scrapy.Field()
    sName = scrapy.Field()
    href = scrapy.Field()
class UIDetailItem(scrapy.Item):
    unname = scrapy.Field()
    code = scrapy.Field()
    location = scrapy.Field()
class UIDetailSchItem(scrapy.Item):
    udName = scrapy.Field()
    sdName = scrapy.Field()
