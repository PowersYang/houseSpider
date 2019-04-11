# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import time

import pymongo
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

from houseSpider.spiders.ftx.community import CommunitySpider as CommunityFtxSpider


class HousespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        collection = item['type']
        dicts = dict(item)

        if isinstance(spider, CommunityFtxSpider):
            # 如果是房天下 需要解析价格走势
            if dicts.get('price_trend'):
                price_trend = dicts.get('price_trend').replace(' ', '')
                del dicts['price_trend']
                price_trend_str = re.sub(r'&.*?&\|', ',', price_trend).replace(']],[[', '],[')[2:-2]
                price_trend_arr = price_trend_str.split('],[')
                for index, arr in enumerate(price_trend_arr):
                    date, price = arr.split(',')
                    if '[' in date:
                        date = date.replace('[', '')
                    if ']' in date:
                        date = date.replace(']', '')
                    date = time.strftime('%Y%m', time.localtime(int(date) / 1000))
                    if index < 12:
                        dicts['comm:' + date] = price
                    elif 12 <= index < 24:
                        dicts['district:' + date] = price
                    else:
                        dicts['city:' + date] = price

        query = {'community_sn': dicts['community_sn']}
        value = {'$set': dicts}
        self.db[collection].update_one(query, value, upsert=True)
        # self.db[collection].insert(dicts)
        return item

    def close_spider(self, spider):
        self.client.close()


class ImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['type'] == 'community_ajk' or item['type'] == 'community_ftx':
            for url in item['images_url']:
                yield Request(url=url, meta={'from_site': item['type'], 'community_sn': item['community_sn']})

    def file_path(self, request, response=None, info=None):
        from_site = request.meta['from_site']
        community_sn = request.meta['community_sn']
        image_name = request.url.split('/')[-2] + '.jpg'
        file_name = u'{0}/{1}/{2}'.format(from_site, community_sn, image_name)
        return file_name

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('图片下载失败！')
        return item
