# -*- coding: utf-8 -*-
import re
import time

import scrapy
from xpinyin import Pinyin
from scrapy import Request

from houseSpider import settings
from houseSpider.items.ftx.trust import trustItem
from houseSpider.tools.tool import tools


class TrustSpider(scrapy.Spider):
    name = 'trust_ftx'
    allowed_domains = ['fang.com']

    p = Pinyin()
    cities = settings.CITIES

    # 生成各个城市的url
    start_urls = ['http://esf.fang.com/housing/']
    for city in cities:
        url = 'http://' + tools.get_pinyin_ftx(city) + 'esf.fang.com/housing/'
        start_urls.append(url)


    def parse(self, response):
        # 根据不同行政区请求
        district_urls = response.css('.qxName a::attr(href)').extract()
        for url in district_urls:
            yield Request(url=response.urljoin(url), callback=self.get_link)

    def get_link(self, response):
        # 获得每个小区详细页的链接并跳转下一页
        links = response.css('div[class="houseList"] dt a::attr(href)').extract()
        for link in links:
            if 'http' not in link:
                link = response.urljoin(link)
            yield Request(url=link + '/chengjiao/', callback=self.parse_content)
        try:
            next_page = response.css('a[id="PageControl1_hlk_next"]::attr(href)').extract_first()
            next_page = response.url + next_page.split('/')[-1]
            yield Request(url=next_page, callback=self.get_link)
        except:
            pass

    def parse_content(self, response):
        # 解析详细页面字段
        table = response.css('div[class="dealSent sentwrap"] tr')
        for index, tr in enumerate(table):
            if index != 0:
                item = trustItem()
                tds = tr.css('td')
                comm_url = response.css('#orginalNaviBox li')[2].css('a::attr(href)').extract_first()

                item['community_sn'] = re.search('.*?/photo/(\d+)', comm_url).group(1)
                item['house_type'] = tds[0].css('.hspro a::text').extract_first()
                item['house_floor'] = tds[0].css('.hspro p')[1].css('::text').extract_first()
                item['house_orientation'] = tds[0].css('.hspro p')[2].css('::text').extract_first()
                item['house_area'] = tds[1].css('::text').extract_first()
                item['sign_time'] = tds[2].css('b::text').extract_first()
                item['trade_price'] = tds[3].css('b::text').extract_first()
                item['unit_price'] = tds[4].css('::text').extract_first()
                item['city'] =  response.css('#agantesfxq_B01_04 a::text').extract()[1][:-3]
                item['up_time'] = int(time.time())
                yield item