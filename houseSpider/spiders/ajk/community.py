# -*- coding: utf-8 -*-
import json
import random
import re
import time

import scrapy
from scrapy import Request
from xpinyin import Pinyin

from houseSpider import settings, useragent
from houseSpider.items.ajk.community import CommunityItem as CommunityAjkItem
from houseSpider.tools.tool import tools


class CommunitySpider(scrapy.Spider):
    name = 'community_ajk'
    allowed_domains = ['anjuke.com']

    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 6
    }

    cities = settings.CITIES
    p = Pinyin()

    headers = {'accept': 'application/json, text/javascript, */*; q=0.01',
               'User-Agent': random.choice(useragent.user_agents)}

    # 生成各个城市的url
    # start_urls = ['https://{city}.anjuke.com/community/'.format(city=p.get_pinyin(city, u'')) for city in cities]
    start_urls = []
    for city in cities:
        url = "https://{c}.anjuke.com/community/".format(c=tools.get_pinyin_ajk(city))
        start_urls.append(url)

    def parse(self, response):
        # 根据行政区请求
        try:
            district_url = response.css('.items span')[1].css('a::attr(href)').extract()
            for index, url in enumerate(district_url):
                # 第0个为“全部小区”
                if index is not 0:
                    yield Request(url=url, callback=self.parse_qx)
        except:
            pass

    def parse_qx(self, response):
        links = response.css('.sub-items a::attr(href)').extract()
        for url in links:
            yield Request(url=url, callback=self.get_link)

    def get_link(self, response):
        links = response.css('div[id="list-content"] div[class="li-info"] a::attr(href)').extract()
        for index, link in enumerate(links):
            if index != 0:
                yield Request(url=link, callback=self.parse_content)
        try:
            # 构造分页信息
            next_page = response.css('.multi-page a::attr(href)').extract()[-1]
            yield Request(url=next_page, callback=self.get_link)
        except:
            print("分页错误...")


    def parse_content(self, response):
        item = CommunityAjkItem()
        item['type'] = 'community_ajk'
        try:
            item['community_sn'] = re.search('.*?(\d+)', response.url).group(1)
        except:
            item['community_sn'] = None

        try:
            item['title'] = response.css('a[class="map-link"]::attr(title)').extract_first()
        except:
            item['title'] = None

        try:
            city = response.css('div[class="p_1180 p_crumbs"] a::text').extract_first()[:-3]
            arr = response.css('span[class="sub-hd"]::text').extract_first().split('-')
            address = '{city}-{district}-{address}'.format(city=city, district=arr[0], address=arr[-1])
            item['address'] = address
        except:
            item['address'] = None

        try:
            arr = response.css('div[class="p_1180 p_crumbs"] a::text').extract()
            item['city'] = arr[1][:-2]
            item['district'] = arr[2][:-2]
        except:
            item['city'] = item['district'] = None

        try:
            attributes = response.css('dl[class="basic-parms-mod"] dd::text').extract()
            item['property_type'] = attributes[0]

            item['property_fee'] = attributes[1]

            item['total_area'] = attributes[2]

            item['total_house'] = attributes[3]

            item['build_age'] = attributes[4]

            item['park_num'] = attributes[5]

            item['volume_rate'] = attributes[6]

            item['green_rate'] = attributes[7]

            item['build_company'] = attributes[8]

            item['property_company'] = attributes[9]
        except:
            pass
        try:
            item['compare'] = response.css('span[class="status down"] i::text').extract_first() + \
                              response.css('span[class="status down"]::text').extract_first()
        except:
            item['compare'] = None

        try:
            item['images_url'] = response.css('div[class="con"] img::attr(src)').extract()
        except:
            item['images_url'] = None

        item['up_time'] = int(time.time())

        if item["community_sn"] is not None:
            yield Request(url='https://anjuke.com/v3/ajax/communityext/?commid={commid}&useflg=onlyForAjax'.format(
                commid=item['community_sn']), callback=self.parse_house, meta={'item': item})
            # yield Request(url='https://anjuke.com/community_ajax/807/price/?cis={cis}'.format(cis=item['community_sn']),
            #               callback=self.parse_price,headers=self.headers, meta={'item': item})
        else:
            yield item

    #
    # def parse_price(self, response):
    #     item = response.meta['item']
    #     res = response.css('body p::text').extract_first()
    #     try:
    #         if res:
    #             if json.loads(res)['msg'] == 'ok':
    #                 data = json.loads(res)['data']
    #                 data = data[item['community_sn']]
    #                 item['price'] = data['mid_price']
    #                 item['compare'] = data['mid_change']
    #                 response.css('.items span')[1].css('a::attr(href)').extract()
    #     except:
    #         pass
    #
    #     yield Request(url='https://anjuke.com/v3/ajax/communityext/?commid={commid}&useflg=onlyForAjax'.format(
    #         commid=item['community_sn']), callback=self.parse_house, meta={'item': item})

    def parse_house(self, response):
        item = response.meta['item']
        res = response.css('body p::text').extract_first()
        try:
            if res:
                data = json.loads(res)['comm_propnum']
                item['sale_house'] = data['saleNum']
                item['rent_house'] = data['rentNum']
        except:
            pass
        yield item
