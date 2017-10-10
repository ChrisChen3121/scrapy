# -*- coding: utf-8 -*-
import scrapy
from lianjia.items import LianjiaItem


class SecondHandSpider(scrapy.spiders.Spider):
    name = 'second_hand'
    allowed_domains = ['lianjia.com']
    handle_httpstatus_list = [302]

    def __init__(self, city_code='sh'):
        self._host = '{}.lianjia.com'.format(city_code)
        self._headers = {'Host': self._host}
        self._city_code = city_code

    def start_requests(self):
        yield scrapy.Request(
            url='http://{}/ershoufang/'.format(self._host),
            headers=self._headers,
            callback=self.parse_cookies)

    def parse_cookies(self, response):
        self._headers["Cookie"] = response.headers.getlist('Set-Cookie')
        yield scrapy.Request(
            url=response.url,
            headers=self._headers,
            callback=self.parse_city_index,
            dont_filter=True)

    def parse_city_index(self, response):
        for node in response.xpath(
                '//div[@id="plateList"]//a[@class="level1-item "]'):
            print(node)
