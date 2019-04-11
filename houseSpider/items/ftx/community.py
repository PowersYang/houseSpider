# -*- coding:utf-8 -*-
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
    # 环比上月
    compare = scrapy.Field()
    # 图片
    images_url = scrapy.Field()
    # 活跃度评级
    activity_rank = scrapy.Field()
    # 板块评级
    area_rank = scrapy.Field()
    # 物业评级
    property_rank = scrapy.Field()
    # 教育评级
    education_rank = scrapy.Field()
    # 价格走势
    price_trend = scrapy.Field()

    up_time = scrapy.Field()
