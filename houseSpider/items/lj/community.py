# -*- coding: utf-8 -*-
import scrapy


class CommunityItem(scrapy.Item):
    type = scrapy.Field()
    # 小区编号
    community_sn = scrapy.Field()
    # 小区名称
    title = scrapy.Field()
    # 均价
    price = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 物业费用
    property_fee = scrapy.Field()
    # 物业公司
    property_company = scrapy.Field()
    # 总户数
    total_house = scrapy.Field()
    # 建造年代
    build_age = scrapy.Field()
    # 开发商
    build_company = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 行政区
    district = scrapy.Field()
    # 总楼栋数
    build_total = scrapy.Field()
    # 建筑类型
    build_type = scrapy.Field()
    # 操作时间
    up_time = scrapy.Field()