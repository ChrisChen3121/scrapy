# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.selector import Selector
from scrapy_splash import SplashRequest

from yscrapy.a51job_items import Company, JDItem


class A51jobSpider(scrapy.Spider):
    name = '51job'
    allowed_domains = ['51job.com']

    #     jobs_lua_script = """
    # function main(splash, args)
    #   splash.images_enabled = false
    #   local ok, reason = splash:go(args.url)
    #   if not ok then
    #     return nil
    #   end
    #   local pages = {}
    #   local not_finished = true
    #   local page_no = 1
    #   while not_finished do
    #     pages[page_no] = splash:html()
    #     local page_nav = splash:select_all('.bk a')
    #     local next_page = page_nav[2]
    #     if next_page then
    #       local href = next_page.info().attributes["href"]
    #       local next_page_no = tonumber(string.sub(href, string.find(href, "%d")))
    #     	if page_no == next_page_no then
    #         not_finished = false
    #       else
    #       	page_no = page_no + 1
    #         next_page:mouse_click()
    #         splash:wait(0.5)
    #       end
    #     else
    #       return nil
    #     end
    #   end
    #   return pages
    # end
    #     """

    def __init__(self):
        # host = 'www.51job.com'
        self._url_root = 'http://jobs.51job.com/'
        self._company_urls = set()

    def start_requests(self):
        yield scrapy.Request(url=self._url_root, callback=self.parse_category)
        # headers=self._headers,
        #callback=self.parse_cookies)

    def parse_category(self, response):
        category_table = response.xpath('//div[@class="filter"]')[2]
        for node in category_table.xpath('.//a/@href'):
            category_url = node.extract()
            yield scrapy.Request(category_url, callback=self.parse_company)
            break  # TODO: for test

    def parse_company(self, response):
        pages_node = response.xpath('//div[@id="cppageno"]')
        current_page_no = pages_node.xpath(
            './ul/li[@class="on"]/text()').extract_first()
        next_page_url = pages_node.xpath(
            './ul/li[@class="bk"]/a/@href').extract()[1]
        match = re.search("\/p(\d+)\/", next_page_url)
        if match:
            page_no_in_next_page = match.group(1)
            if int(current_page_no) != int(page_no_in_next_page):
                yield scrapy.Request(
                    next_page_url, callback=self.parse_company)
        for node in response.xpath('//a[@class="name"]/@href'):
            compnay_url = node.extract()
            compnay_url = re.sub(r'(http:\/\/.+?\/).+(\/.+html)', r'\1all\2',
                                 compnay_url)
            if compnay_url not in self._company_urls:
                self._company_urls.add(compnay_url)
                yield scrapy.Request(
                    compnay_url, callback=self.parse_company_page)

    def parse_company_page(self, response):
        company_info = self._parse_company_info(response)
        if company_info:
            yield company_info
            # yield SplashRequest(
            #     url=response.url,
            #     # headers=self._headers,
            #     callback=self._parse_jobs,
            #     endpoint='execute',
            #     meta={"company_url": response.url},
            #     args={
            #         'lua_source': self.jobs_lua_script,
            #         'timeout': 3600,
            #     })

    def _parse_company_info(self, response):
        company_info = Company()
        company_head_node = response.xpath(
            '//div[@class="tHeader tHCop"]/div[starts-with(@class, "in ")]')
        company_info['link'] = response.url
        company_info['name'] = company_head_node.xpath(
            './h1/text()').extract_first()
        company_summary_str = company_head_node.xpath(
            './p[@class="ltype"]/text()').extract_first()
        if not company_summary_str:
            self.logger.error(
                "wrong summary string, url:{}".format(response.url))
            return None
        summary_list = company_summary_str.split('|')
        summary_list = [x.strip() for x in summary_list]
        if len(summary_list) != 3:
            self.logger.error("wrong summary list, len {}, url:{}".format(
                len(summary_list), response.url))
            self.logger.error(summary_list)
            return None
        company_info['_type'] = summary_list[0]
        company_info['scale'] = summary_list[1]
        company_info['field'] = summary_list[2]
        company_info['description'] = response.xpath(
            '//div[@class="tBorderTop_box"]//p/text()').extract_first().strip(
            )
        address_info = response.xpath(
            '//div[@class="tBorderTop_box bmsg"]//p[@class="fp"]/text()'
        ).extract()
        if len(address_info) > 1:
            company_info['address'] = address_info[1].strip()
        company_info['total_available'] = response.xpath(
            '//div[@class="dw_page"]//input[@id="hidTotal"]/@value'
        ).extract_first()
        return company_info

    # def _parse_jobs(self, response):
    #     pages = response.data
    #     for page in pages.values():
    #         page = Selector(text=page)
    #         company_link = response.meta["company_url"]
    #         company_name = page.xpath(
    #             '//div[@class="tHeader tHCop"]/div[starts-with(@class, "in ")]/h1/text()'
    #         ).extract_first()
    #         for job_node in page.xpath('//div[@class="el"]'):
    #             job_item = JDItem()
    #             job_item["company_name"] = company_name
    #             job_item["company_link"] = company_link
    #             job_item["title"] = self.__return_if_exist(
    #                 job_node.xpath('./p[@class="t1"]/a/@title').extract())
    #             job_item["link"] = self.__return_if_exist(
    #                 job_node.xpath('./p[@class="t1"]/a/@href').extract())
    #             job_item["area"] = self.__return_if_exist(
    #                 job_node.xpath('./span[@class="t3"]/text()').extract())
    #             job_item["salary"] = self.__return_if_exist(
    #                 job_node.xpath('./span[@class="t4"]/text()').extract())
    #             job_item["publish_date"] = self.__return_if_exist(
    #                 job_node.xpath('./span[@class="t5"]/text()').extract())
    #             comb_field_str = self.__return_if_exist(
    #                 job_node.xpath('./span[@class="t2"]/text()').extract())
    #             comb_fields = [field.strip() for field in comb_field_str.split('|')]
    #             for comb_field in comb_fields:
    #                 self._parse_comb_field(job_item, comb_field)
    #             yield job_item

    # def _parse_comb_field(self, job_item, comb_field):
    #     if re.match("\d+", comb_field):
    #         job_item["experience"] = comb_field
    #     else:
    #         m = re.search("\d+", comb_field)
    #         if m:
    #             job_item["vacancy"] = m.group(0)
    #         else:
    #             job_item["education"] = comb_field

    # def __return_if_exist(self, node_text):
    #     if len(node_text) > 0:
    #         return node_text[0]
    #     else:
    #         return None
