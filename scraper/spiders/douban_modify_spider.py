# coding=utf-8
from __future__ import unicode_literals

import scrapy
from mongoengine import connect

from yuntu.documents import Book


class DoubanModifySpider(scrapy.Spider):
    # 定义爬虫的名称
    name = "douban_spider"

    def __init__(self, **kwargs):
        super(DoubanModifySpider, self).__init__(**kwargs)
        connect('django')

    def start_requests(self):
        for book in Book.objects():
            url = 'https://book.douban.com/subject_search?search_text=' + book.isbn
            yield scrapy.Request(url=url)

    def parse(self, response):
        info = response.xpath('//*[@id="content"]/div/div[1]/ul/li/div[2]/div[1]/text()').extract_first().strip()
        print info
        print
