# -*- coding: utf-8 -*-

import scrapy

class Company(scrapy.Item):
    name = scrapy.Field()
    _type = scrapy.Field()
    scale = scrapy.Field()
    field = scrapy.Field()
    description = scrapy.Field()
    address = scrapy.Field()
    link = scrapy.Field()
    total_available = scrapy.Field()

class JDItem(scrapy.Item):
    title = scrapy.Field()
    experience = scrapy.Field()
    education = scrapy.Field()
    vacancy = scrapy.Field()
    company_name = scrapy.Field()
    company_link = scrapy.Field()
    publish_date = scrapy.Field()
    job_description = scrapy.Field()
    link = scrapy.Field()
    area = scrapy.Field()
    salary = scrapy.Field()
