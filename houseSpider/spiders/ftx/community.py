# -*- coding: utf-8 -*-
import re
import time

import scrapy
from scrapy import Request
from xpinyin import Pinyin

from houseSpider import settings
from houseSpider.items.ftx.community import CommunityItem as CommunityFtxItem
from houseSpider.tools.tool import tools


class CommunitySpider(scrapy.Spider):
    name = 'community_ftx'
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
        for index, url in enumerate(district_urls):
            # 第一个为条件不限
            if index != 0:
                yield Request(url=response.urljoin(url), callback=self.parse_qx)

    def parse_qx(self, response):
        links = response.css('.contain a::attr(href)').extract()
        rep_str = response.url.split('/')[-2]
        for index, link in enumerate(links):
            # 第一个为条件不限
            if index != 0:
                url = response.url.replace(rep_str, link.split('/')[2])
                yield Request(url=url, callback=self.get_link)

    def get_link(self, response):
        # 获得每个小区详细页的链接并跳转下一页
        links = response.css('div[class="houseList"] dt a::attr(href)').extract()
        for link in links:
            if 'http' not in link:
                link = response.urljoin(link)
            yield Request(url=link, callback=self.parse_content)

        try:
            # 构造分页信息
            next_page = response.css('a[id="PageControl1_hlk_next"]::attr(href)').extract_first()
            next_page = response.url + next_page.split('/')[-1]
            yield Request(url=next_page, callback=self.get_link)
        except:
            print("分页错误...")

    def parse_content(self, response):
        # 解析详细页面字段
        item = CommunityFtxItem()
        item['type'] = 'community_ftx'
        try:
            community_sn = response.css('div[class="bannerbg_pos"] a::attr(href)').extract_first()
            community_sn = re.search('.*?(\d+)', community_sn).group(1)
            item['community_sn'] = community_sn
        except:
            item['community_sn'] = None

        try:
            item['title'] = response.css('div[class="Rbigbt clearfix"] b::text').extract_first()
        except:
            item['title'] = None

        try:
            item['price'] = response.css('span[class="prib"]::text').extract_first()
        except:
            item['price'] = None

        try:
            text = response.css('a[class="gray9"]::text').extract()
            address = text[1][:-3] + '-' + text[3][:-5] + '-'
            str = response.css('div[class="Rinfolist"] ul li:nth-child(6)::text').extract_first()
            item['address'] = address + str
        except:
            item['address'] = None

        try:
            item['property_company'] = response.css('div[class="Rinfolist"] li:nth-child(8)::text').extract_first()
        except:
            item['property_company'] = None

        try:
            item['total_house'] = response.css('div[class="Rinfolist"] li:nth-child(5)::text').extract_first()
        except:
            item['total_house'] = None

        try:
            item['build_age'] = response.css('div[class="Rinfolist"] li:nth-child(1)::text').extract_first()
        except:
            item['build_age'] = None

        try:
            item['build_company'] = response.css('div[class="Rinfolist"] li:nth-child(9)::text').extract_first()
        except:
            item['build_company'] = None

        try:
            arr = response.css('a[class="gray9"]::text').extract()
            item['city'] = arr[1][:-3]
            item['district'] = arr[3][:-5]
        except:
            item['city'] = item['district'] = None

        try:
            item['build_type'] = response.css('div[class="Rinfolist"] li:nth-child(3)::text').extract_first()
        except:
            item['build_type'] = None

        try:
            item['build_total'] = response.css('div[class="Rinfolist"] li:nth-child(7)::text').extract_first()
        except:
            item['build_total'] = None

        try:
            item['compare'] = response.css('span[class="hb"] em::text').extract_first()
        except:
            item['compare'] = None

        try:
            ranks = response.css('div[class="xqgrade clearfix"] div[class="s3"] p::text').extract()
            item['activity_rank'] = ranks[0]
            item['area_rank'] = ranks[1]
            item['property_rank'] = ranks[2]
            item['education_rank'] = ranks[3]
        except:
            item['activity_rank'] = item['area_rank'] = item['property_rank'] = item['education_rank'] = None

        try:
            item['images_url'] = response.css(
                'div[id="kesfxqxq_A01_01_01"] li a img[class="datu"]::attr(src)').extract()
        except:
            item['images_url'] = None

        item['up_time'] = int(time.time())

        # 小区编号和城市解析成功才能请求价格走势
        if item['community_sn'] is None or item['city'] is None:
            yield item
        else:
            # 创建价格走势请求链接
            try:
                district = response.css('a[class="gray9"]::text').extract()[3][:-5]

                price_url = 'http://pinggus.fang.com/RunChartNew/MakeChartData?newcode={community_sn}&city={city}' \
                            '&district={district}'.format(community_sn=item['community_sn'], city=item['city'],
                                                          district=district)
                price_url = price_url.encode('unicode_escape').decode().replace("\\u", "%u")
                yield Request(url=price_url, callback=self.get_price_trend, meta={'item': item})
            except:
                # 如果请求失败返回其它字段
                yield item

    def get_price_trend(self, response):
        # 解析价格走势
        item = response.meta['item']
        try:
            item['price_trend'] = response.css('body p::text').extract_first()
            yield item
        except:
            pass
