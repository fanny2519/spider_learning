# 管道
"""
钩子函数（回调函数）（callback）

"""
import pymysql as pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import openpyxl
import pymysql


class DBSpiderLearningPipeline:
    def __init__(self):
        self.conn = pymysql.connect(host='localhost',
                                    port=3306, user='root', password='123',
                                    database='house_price'
                                    )
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        Building_orientation = item.get('Building_orientation', '暂无数据')
        Building_structure = item.get('Building_structure', '暂无数据')
        Building_type = item.get('Building_type', '暂无数据')
        Cell_name = item.get('Cell_name', '暂无数据')
        Decoration_condition = item.get('Decoration_condition', '暂无数据')
        Equipped_with_elevator = item.get('Equipped_with_elevator', '暂无数据')
        Floor_area = item.get('Floor_area', '暂无数据')
        Floor_height = item.get('Floor_height', '暂无数据')
        House_type_structure = item.get('House_type_structure', '暂无数据')
        Housing_type = item.get('Housing_type', '暂无数据')
        In_casing_area = item.get('In_casing_area', '暂无数据')
        Local_area = item.get('Local_area', '暂无数据')
        Proportion_of_ladder_households = item.get('Proportion_of_ladder_households', '暂无数据')
        Total_price = item.get('Total_price', '0')
        Unit_price = item.get('Unit_price', '0')
        Heating_method = item.get('Heating_method', '暂无数据')
        Floor = item.get('Floor', '暂无数据')
        City = item.get('City', '暂无数据')
        Time = item.get('Time', '暂无数据')
        Title = item.get('Title', '暂无数据')
        Url = item.get('Url', '暂无数据')

        self.cursor.execute(
            'insert into sh_price (Building_orientation, Building_structure, Building_type, Cell_name, '
            'Decoration_condition, Equipped_with_elevator, Floor_area, Floor_height, '
            'House_type_structure, Housing_type, In_casing_area, Local_area, '
            'Proportion_of_ladder_households, Total_price, Unit_price, Floor, '
            'City, Heating_method, Time, Title, Url) values('
            '%s, %s, %s, %s, %s, %s, %s, %s, '
            '%s, %s, %s, %s, %s, %s, %s, %s, '
            '%s, %s, %s, %s, %s)',
            (Building_orientation, Building_structure, Building_type, Cell_name,
             Decoration_condition, Equipped_with_elevator, Floor_area, Floor_height,
             House_type_structure, Housing_type, In_casing_area, Local_area,
             Proportion_of_ladder_households, Total_price, Unit_price, Floor,
             City, Heating_method, Time, Title, Url)
        )
        return item


class ExcelSpiderLearningPipeline:
    # 初始化方法，创建工作簿、工作表
    def __init__(self):
        self.wb = openpyxl.Workbook()
        # wb.create_sheet()  # 创建一张新的工作表
        self.ws = self.wb.active
        self.ws.title = '武汉房价'
        self.ws.append(('Housing_type', 'floor', 'Floor_area', 'House_type_structure',
                        'In_casing_area', 'Building_type', 'Building_orientation', 'Building_structure',
                        'Decoration_condition', 'Proportion_of_ladder_households', 'Equipped_with_elevator',
                        'Floor_height', 'Proportion_of_ladder_households', 'Total_price', 'Unit_price', 'floor',
                        'city'))

    # 数据处理
    def process_item(self, item, spider):
        """
        'Housing_type', 'floor', 'Floor_area', 'House_type_structure',
        'In_casing_area', 'Building_type', 'Building_orientation', 'Building_structure',
        'Decoration_condition', 'Proportion_of_ladder_households', 'Equipped_with_elevator',
        'Floor_height'
        """
        Building_orientation = item.get('Building_orientation', '')
        Building_structure = item.get('Building_structure', '')
        Building_type = item.get('Building_type', '')
        Cell_name = item.get('Cell_name', '')
        Decoration_condition = item.get('Decoration_condition', '')
        Equipped_with_elevator = item.get('Equipped_with_elevator', '')
        Floor_area = item.get('Floor_area', '')
        Floor_height = item.get('Floor_height', '')
        House_type_structure = item.get('House_type_structure', '')
        Housing_type = item.get('Housing_type', '')
        In_casing_area = item.get('In_casing_area', '')
        Local_area = item.get('Local_area', '')
        Proportion_of_ladder_households = item.get('Proportion_of_ladder_households', '')
        Total_price = item.get('Total_price', '0')
        Unit_price = item.get('Unit_price', '0')
        floor = item.get('floor', '')

        self.ws.append((Building_orientation, Building_structure, Building_type, Cell_name,
                        Decoration_condition, Equipped_with_elevator, Floor_area, Floor_height,
                        House_type_structure, Housing_type, In_casing_area, Local_area,
                        Proportion_of_ladder_households, Total_price, Unit_price, floor))

        return item

    # 当爬虫关闭时保存工作表
    def close_spider(self, spider):
        # 保存工作表
        self.wb.save('武汉房价.xlsx')
