# 蜘蛛程序
import time

import scrapy
from scrapy import Selector
from scrapy.http import HtmlResponse

from spider_learning.items import HouseItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


# 运行方式：
# scrapy crawl lianjia_bj
# 格式：scrapy crawl 【name】

# 存入csv：scrapy crawl lianjia_bj -o lianjia_bj.csv
class LianjiaSpider_bj(scrapy.Spider):
    name = "lianjia_bj"
    allowed_domains = ["bj.lianjia.com"]
    # start_urls = ["https://cd.lianjia.com/ershoufang/106115530736.html"]

    # 一级页面（一共一百页）
    def start_requests(self):
        for page in range(21, 101):
            yield scrapy.Request(url="https://bj.lianjia.com/ershoufang/pg" + str(page), callback=self.parse)
            time.sleep(1)

    # 二级页面（详情页）
    def parse(self, response: HtmlResponse, **kwargs):
        sel = Selector(response)
        list_urls = sel.css('#content > div.leftContent > ul > li')
        for a_url in list_urls:
            self.son_url = a_url.css('a::attr(href)').extract_first()
            time.sleep(1)
            # print(url)
            # 只写函数名 parse_detail

            yield scrapy.Request(url=self.son_url, callback=self.parse_detail,
                                 errback=self.errback_httpbin,
                                 dont_filter=True
                                 )

    def parse_detail(self, response):
        print("_____________________________________________________________")
        time.sleep(1)
        sel2 = Selector(response)
        house_item = HouseItem()
        # 房屋户型 所在楼层 建筑面积 户型结构
        # 套内面积 建筑类型 房屋朝向 建筑结构
        # 装修情况 梯户比例 配备电梯 楼层高度
        house_title = ['Housing_type', 'Floor', 'Floor_area', 'House_type_structure',
                        'In_casing_area', 'Building_type', 'Building_orientation', 'Building_structure',
                        'Decoration_condition', 'Proportion_of_ladder_households', 'Heating_method',
                        'Equipped_with_elevator',
                        'Floor_height']
        list_items = sel2.css('#introduction > div > div > div.base > div.content > ul > li')
        # print(list_items)
        if len(list_items) >= 13:
            for item in range(13):
                describes = list_items[item].xpath("text()").extract()[1]
                describes_processed = describes.strip().replace(" ", "").split("\"")
                house_item[house_title[item]] = describes_processed
        elif len(list_items) < 13:
            for item in range(len(list_items)):
                describes = list_items[item].xpath("text()").extract()[1]
                describes_processed = describes.strip().replace(" ", "").split("\"")
                house_item[house_title[item]] = describes_processed
        house_item['Total_price'] = sel2.css('body > div.overview > div.content > div.price-container > div > '
                                            'span.total::text').extract_first()  # 总价

        # print(house_item['Total_price'])

        house_item['Unit_price'] = sel2.css('body > div.overview > div.content > div.price-container > div > '
                                            'div.text > div.unitPrice > span::text').extract_first()  # 单价

        # 小区名称
        house_item['Cell_name'] = sel2.css('body > div.overview > div.content > div.aroundInfo > div.communityName > '
                                            'a.info::text').extract_first()

        # 所在区域
        house_item['Local_area'] = sel2.css('body > div.overview > div.content > div.aroundInfo > div.areaName > '
                                            'span.info > a:nth-child(1)::text').extract_first()

        house_item['City'] = '北京'
        # print(house_item['City'])
        house_item['Time'] = sel2.xpath('//*[@id="introduction"]/div/div/div[2]/div[2]/ul/li[1]/span[2]/text()').extract()
        # print(house_item['Time'])

        house_item['Title'] = sel2.css('body > div.sellDetailHeader > div > div > div.title > h1::text').extract_first()

        house_item['Url'] = str(self.son_url)

        yield house_item

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.info(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.info('HttpError错误 on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.info('DNSLookupError错误 on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.info('TimeoutError错误 on %s', request.url)

