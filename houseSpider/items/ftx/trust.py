# -*- coding: utf-8 -*-
import scrapy
from scrapy import Field


class trustItem(scrapy.Item):
    # 小区编号
    community_sn = Field()
    # 朝向
    house_orientation = Field()
    # 房屋类型
    house_type = Field()
    # 楼层
    house_floor = Field()
    # 面积
    house_area = Field()
    # 成交价
    trade_price = Field()
    # 单价
    unit_price = Field()
    # 城市
    city = Field()
    # 签约时间
    sign_time = Field()
    # 获取时间
    up_time = Field()
