# -*- coding: utf-8 -*-
import json
import re
import time

import scrapy
from scrapy import Request
from xpinyin import Pinyin

from houseSpider import settings
from houseSpider.items.lj.community import CommunityItem as CommunityLjItem
from houseSpider.tools.tool import tools


class CommunitySpider(scrapy.Spider):
    name = 'community_lj'
    allowed_domains = ['lianjia.com']

    cities = settings.CITIES
    p = Pinyin()

    custom_settings = {
        'ITEM_PIPELINES': {
            'houseSpider.pipelines.HousespiderPipeline': 300,
            'houseSpider.pipelines.MongoPipeline': 400,
        }
    }
    start_urls = []
    for city in cities:
        url = 'https://{city}.lianjia.com/xiaoqu/'.format(city=tools.get_pinyin_lj(city))
        start_urls.append(url)

    def parse(self, response):
        # 根据不同行政区请求
        district_urls = response.css('div[data-role="ershoufang"] a::attr(href)').extract()
        for url in district_urls:
            district_url = response.url + url[8:]

            yield Request(url=district_url, callback=self.parse_qx)

    def parse_qx(self, response):
        links = response.css('div[data-role="ershoufang"] a::attr(href)').extract()
        for link in links:
            if 'http' not in link:
                link = response.urljoin(link)
                yield Request(url=link, callback=self.get_link)

    def get_link(self, response):
        node_list = response.css('ul[class="listContent"] a[class="img"]::attr(href)').extract()
        for url in node_list:
            yield Request(url=url, callback=self.parse_content)

        try:
            # 构造分页信息
            page_info = response.css('div[class="page-box house-lst-page-box"]::attr(page-data)').extract_first()
            if page_info is not None:
                js = json.loads(page_info)
                if js is not None:
                    total_page = int(js.get('totalPage'))
                    for url in node_list:
                        for page in range(1, total_page + 1):
                            yield Request(url=url + 'pg' + str(total_page), callback=self.get_link)
        except:
            print("分页错误...")

    def parse_content(self, response):
        item = CommunityLjItem()

        item['type'] = 'community_lj'
        try:
            item['community_sn'] = re.search('.*?(\d+)', response.url).group(1)
        except:
            item['community_sn'] = None

        try:
            item['title'] = response.css('h1[class="detailTitle"]::text').extract_first()
        except:
            item['title'] = None

        try:
            item['price'] = response.css('span[class="xiaoquUnitPrice"]::text').extract_first()
        except:
            item['price'] = None

        try:
            text = response.css('div[class="fl l-txt"] a::text').extract()
            address = text[1][:-2] + '-' + text[2][:-2] + '-' + response.css(
                'div[class="detailDesc"]::text').extract_first()
            item['address'] = address
        except:
            item['address'] = None

        try:
            xiaoquInfo = response.css('span[class="xiaoquInfoContent"]::text').extract()
        except:
            item['property_fee'] = item['property_company'] = item['total_house'] = item['build_age'] = \
                item['build_company'] = item['build_total'] = item['build_type'] = None
        else:
            try:
                item['property_fee'] = xiaoquInfo[2]
            except:
                item['property_fee'] = None

            try:
                item['property_company'] = xiaoquInfo[3]
            except:
                item['property_company'] = None

            try:
                item['total_house'] = xiaoquInfo[6]
            except:
                item['total_house'] = None

            try:
                item['build_age'] = xiaoquInfo[0]
            except:
                item['build_age'] = None

            try:
                item['build_company'] = xiaoquInfo[4]
            except:
                item['build_company'] = None

            try:
                item['build_total'] = xiaoquInfo[5]
            except:
                item['build_total'] = None

            try:
                item['build_type'] = xiaoquInfo[1]
            except:
                item['build_type'] = None

        try:
            str = response.css('div[class="fl l-txt"] a::text').extract()
            item['city'] = str[1][:-2]
            item['district'] = str[2][:-2]
        except:
            item['city'] = item['district'] = None

        item['up_time'] = int(time.time())

        yield item
