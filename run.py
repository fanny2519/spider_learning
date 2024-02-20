import scrapy
from scrapy.crawler import CrawlerProcess





from spider_learning.spiders.lianjia_beijing_bj import LianjiaSpider_bj
from spider_learning.spiders.lianjia_四川_cd import LianjiaSpider_cd
from spider_learning.spiders.lianjia_广东_gz import LianjiaSpider_gz
from spider_learning.spiders.lianjia_广西_nn import LianjiaSpider_nn
from spider_learning.spiders.lianjia_福建_fz import LianjiaSpider_fz

# 启动爬虫

process = CrawlerProcess()
process.crawl(LianjiaSpider_bj)
process.crawl(LianjiaSpider_cd)
# process.crawl(LianjiaSpider_gz)
# process.crawl(LianjiaSpider_nn)
# process.crawl(LianjiaSpider_fz)


process.start()

