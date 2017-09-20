# -*- coding: utf-8 -*-
import scrapy
from yscrapy.items import EducationCategoryItem
from bs4 import BeautifulSoup


class DianpingSpider(scrapy.Spider):
    name = 'dianping'
    allowed_domains = ['dianping.com']
    start_urls = ['http://www.dianping.com']

    def parse(self, response):
        pass


class EducationCategorySpider(DianpingSpider):
    name = 'education_category'
    allowed_domains = ['dianping.com']
    start_urls = ['http://www.dianping.com/search/category/1/75']

    def parse(self, response):
        bsObj = BeautifulSoup(response.text)
        node = bsObj.find("div", {"class": "nc-items"})
        for child in node.findAll("a"):
            item = EducationCategoryItem()
            item["id_"] = child.attrs["href"].split("/")[-1]
            item["name"] = child.span.text
            item['url'] = child.attrs["href"]
            yield item
