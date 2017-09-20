# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class EducationCategoryItem(YScrapyItem):
    id_ = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
