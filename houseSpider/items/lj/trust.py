# -*- coding: utf-8 -*-
import scrapy
from scrapy import Field

class trustItem(scrapy.Item):
    # 小区编号
    community_sn = Field()
    # 房屋朝向(东南 / 南)
    house_orientation = Field()
    # 户型
    house_type = Field()
    # 楼层
    house_floor = Field()
    # 房屋总面积
    house_area = Field()
    # 成交价格
    trade_price = Field()
    # 单价
    unit_price = Field()
    # 城市
    city = Field()
    # 更新时间
    up_time = Field()
    # 房屋编号
    house_sn = Field()
    # 标题
    title = Field()
    # 图片
    images = Field()
    # 地址
    address = Field()
    # 建造年代
    build_age = Field()
    # 建筑类型(板楼 / 塔楼)
    build_type = Field()
    # 建筑结构(钢混结构)
    build_fabric = Field()
    # 房屋实际面积
    house_real_area = Field()
    # 房型结构(平层、跃层)
    house_fabric = Field()
    # 装修程度(简装 / 中装)
    house_decoration = Field()
    # 产权年限
    house_property = Field()
    # 房屋用途(商用 / 普通住宅)
    house_purpose = Field()
    # 房屋年限
    house_age = Field()
    # 交易权属(商品房 / 限价商品房)
    trade_type = Field()
    # 挂牌时间 / 发布时间
    trade_time = Field()
    # 关注人数
    trade_follow = Field()
    # 成交周期
    trade_cycle = Field()
    # 调价次数
    trade_adjust = Field()
    # 带看次数
    trade_look = Field()
    # 访问次数
    trade_visit = Field()
    # 梯户比例(一梯两户 / 两梯四户)
    elevator_rate = Field()
    # 电梯配置(有 / 无)
    elevator_status = Field()


