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
    # 物业类型
    property_type = scrapy.Field()
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
    # 环比上月
    compare = scrapy.Field()
    # 图片
    images_url = scrapy.Field()
    # 容积率
    volume_rate = scrapy.Field()
    # 绿化率
    green_rate = scrapy.Field()
    # 总面积
    total_area = scrapy.Field()
    # 停车位
    park_num = scrapy.Field()
    # 二手房总数
    sale_house = scrapy.Field()
    # 租房总数
    rent_house = scrapy.Field()
    # 操作时间
    up_time = scrapy.Field()
