# coding=utf-8
from __future__ import unicode_literals

# import datetime
import scrapy


class AbstractSpider(scrapy.Spider):
    # 定义爬虫的名称
    name = "yuntu_library_spider"
    download_delay = 0.18
    allowed_domains = ["http://www.xxxxxx.com"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.Pipeline': 300,
        }
    }

    def __init__(self, **kwargs):
        super(AbstractSpider, self).__init__(**kwargs)

    def parse(self, response):
        pass

    def start_requests(self):
        yield scrapy.Request(url='', callback=self.parse_page, meta={})

    def parse_page(self, response):
        pass
