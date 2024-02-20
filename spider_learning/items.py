# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Total_price = scrapy.Field()
    Unit_price = scrapy.Field()
    Cell_name = scrapy.Field()
    Local_area = scrapy.Field()
    Housing_type = scrapy.Field()
    Floor = scrapy.Field()
    Floor_area = scrapy.Field()
    House_type_structure = scrapy.Field()
    In_casing_area = scrapy.Field()
    Building_type = scrapy.Field()
    Building_orientation = scrapy.Field()
    Building_structure = scrapy.Field()
    Decoration_condition = scrapy.Field()
    Proportion_of_ladder_households = scrapy.Field()
    Equipped_with_elevator = scrapy.Field()
    Heating_method = scrapy.Field()
    Floor_height = scrapy.Field()
    City = scrapy.Field()
    Time = scrapy.Field()
    Title = scrapy.Field()
    Url = scrapy.Field()
    # 总价 单价 小区名称 所在区域
    # 房屋户型 所在楼层 建筑面积 户型结构
    # 套内面积 建筑类型 房屋朝向 建筑结构
    # 装修情况 梯户比例 配备电梯 楼层高度