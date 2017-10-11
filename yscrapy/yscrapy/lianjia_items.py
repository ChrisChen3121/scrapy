# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SecondHandItem(scrapy.Item):
    _id = scrapy.Field()
    province = scrapy.Field()
    area = scrapy.Field()
    title = scrapy.Field()
    community_id = scrapy.Field()
    # longitude = scrapy.Field()
    # latitude = scrapy.Field()
    # community = scrapy.Field()
    structure = scrapy.Field()
    floor = scrapy.Field()
    direction = scrapy.Field()
    total_area = scrapy.Field()
    build_time = scrapy.Field()
    total_price = scrapy.Field()
    avg_price = scrapy.Field()
    city = scrapy.Field()
    decorator = scrapy.Field()
    elevator = scrapy.Field()

class NewEstateItem(scrapy.Item):
    _id = scrapy.Field()
    # Not implemented yet

class CommunityItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    property = scrapy.Field()
    builder = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()
    build_year = scrapy.Field()
    avg_price = scrapy.Field()
    address = scrapy.Field()
