# -*- coding: utf-8 -*-
import scrapy
from yscrapy.lianjia_items import SecondHandItem


class LianjiaSpider(scrapy.spiders.Spider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    handle_httpstatus_list = [302]

    def __init__(self, city_code='sh'):
        host = '{}.lianjia.com'.format(city_code)
        self._url_root = 'http://{}'.format(host)
        self._headers = {'Host': host}
        self._city_code = city_code

    def start_requests(self):
        yield scrapy.Request(
            url='{}/ershoufang/'.format(self._url_root),
            headers=self._headers,
            callback=self.parse_cookies)

    def parse_cookies(self, response):
        self._headers["Cookie"] = response.headers.getlist('Set-Cookie')
        yield scrapy.Request(
            url=response.url,
            headers=self._headers,
            callback=self.parse_city_page,
            dont_filter=True)

    def parse_city_page(self, response):
        city = response.xpath(
            '//div[@class="m-side-bar"]//span[@class="header-text"]/text()'
        ).extract_first()
        for node in response.xpath(
                '//div[@id="plateList"]//a[@class="level1-item "]'):
            item = SecondHandItem()
            item['city'] = city
            item['province'] = node.xpath("text()").extract_first()
            meta = {'item': item}
            sublink = node.xpath('@href').extract_first()
            if sublink:
                yield scrapy.Request(
                    url='{}{}'.format(self._url_root, sublink),
                    headers=self._headers,
                    meta=meta,
                    callback=self.parse_province_page)
            break

    def parse_province_page(self, response):
        for node in response.xpath(
                '//div[@class="level2 gio_plate"]//a[@gahref!="plate-nolimit"]'
        ):
            item = response.meta["item"]
            item['area'] = node.xpath("text()").extract_first()
            sublink = node.xpath('@href').extract_first()
            if sublink:
                yield scrapy.Request(
                    url='{}{}'.format(self._url_root, sublink),
                    headers=self._headers,
                    meta=response.meta,
                    callback=self.parse_estate_list)
            break

    def parse_estate_list(self, response):
        for node in response.xpath('//ul[@class="js_fang_list"]/li'):
            # item = response.meta['item'].copy()
            detail_link = node.xpath('a/@href').extract_first()
            meta = response.meta
            meta['item']['_id'] = detail_link.split('/')[-1].split('.')[0]
            yield scrapy.Request(
                url='{}{}'.format(self._url_root, detail_link),
                headers=self._headers,
                meta=meta,
                callback=self.parse_estate_detail)
            break

    def parse_estate_detail(self, response):
        item = response.meta['item'].copy()
        item['title'] = response.xpath(
            '//h1[@class="header-title"]/text()').extract_first()
        # item['community'] = response.xpath(
        #     '//span[@class="maininfo-estate-name"]/a[@gahref="ershoufang_gaiyao_xiaoqu_link"]/text()'
        # ).extract_first()
        main_price_node = response.xpath(
            '//aside[@class="content-side"]/div[@class="maininfo-price maininfo-item"]'
        )
        item['total_price'] = main_price_node.xpath(
            'div[@class="price-total"]/span[@class="price-num"]/text()'
        ).extract_first()
        item['avg_price'] = main_price_node.xpath(
            'div[@class="price-unit"]/p[@class="price-unit-num"]/span/text()'
        ).extract_first()
        main_info_node = response.xpath(
            '//aside[@class="content-side"]/ul[@class="maininfo-main maininfo-item"]'
        )
        item['direction'] = main_info_node.xpath(
            'li[@class="main-item u-tc"]//p[@class="u-fz20 u-bold"]/text()'
        ).extract_first().strip()
        item['floor'] = main_info_node.xpath(
            'li[@class="main-item u-tc"]//p[@class="u-mt8 u-fz12"]/text()'
        ).extract_first()
        item['total_area'] = main_info_node.xpath(
            'li[@class="main-item u-tr"]//p[@class="u-fz20 u-bold"]/text()'
        ).extract_first()
        item['build_time'] = main_info_node.xpath(
            'li[@class="main-item u-tr"]//p[@class="u-mt8 u-fz12"]/text()'
        ).extract_first().strip()
        basic_info_node = response.xpath(
            '//div[@class="content-main module-tb"]')
        item['structure'] = basic_info_node.xpath(
            './/div[@class="module-col baseinfo-col2"]//ul[@class="baseinfo-tb"]/'
            'li[1]/span[@class="item-cell"]/text()').extract_first()
        item['elevator'] = basic_info_node.xpath(
            './/div[@class="module-col baseinfo-col2"]//ul[@class="baseinfo-tb"]/'
            'li[2]/span[@class="item-cell"]/text()').extract_first()
        item['decorator'] = basic_info_node.xpath(
            './/div[@class="module-col baseinfo-col3"]//ul[@class="baseinfo-tb"]/'
            'li[2]/span[@class="item-cell"]/text()').extract_first()
        # item['latitude'] = response.xpath(
        #     '//div[@id="aroundApp"]/@latitude').extract_first()
        # item['longitude'] = response.xpath(
        #     '//div[@id="aroundApp"]/@longitude').extract_first()
        yield item
