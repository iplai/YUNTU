# encoding=utf-8
import json
import scrapy
import time
from scrapy import Selector
from scrapy.http import Request

from ..items import SheyingArticleItem, SheyingCateItem


class SheyingSpider(scrapy.Spider):
    name = "sheyingSpider"
    start_urls = ["http://sheying.sioe.cn/"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_project.pipelines.SheyingPipeline': 300,
        }
    }

    def __init__(self, name=None, **kwargs):
        super(SheyingSpider, self).__init__(name=None, **kwargs)

    def parse(self, response):
        """获取一级目录"""
        sel = Selector(response)
        first_cate_item = SheyingCateItem()
        for block in sel.css('div.node'):
            try:
                first_cate_item['name'] = block.xpath('div[@class="title"]/a/text()').extract()[0]
                first_cate_item['link'] = block.xpath('div[@class="title"]/a/@href').extract()[0]
                first_cate_item['level'] = '1'
                first_cate_item['up_level'] = None
                yield first_cate_item
                url = first_cate_item['link']
                name = first_cate_item['name']
                yield Request(url, callback=self.get_second_cate, meta={'first_cate': name, 'second_cate': None})
            except Exception, e:
                self.logger.warning(str(e))

    def get_second_cate(self, response):
        """获取二级目录"""
        first_cate = response.meta['first_cate']
        second_cate = response.meta['second_cate']
        sel = Selector(response)
        # 若网页中存在list，说明没有二级目录，直接是文章列表
        if len(sel.css('div.list')) > 0:
            # 爬取该目录下的第一篇文章
            url = sel.css('div.title').xpath('h2/a/@href').extract()[0]
            # yield Request(url, self.get_article, meta={'first_cate': first_cate, 'second_cate': second_cate})
            return
        if first_cate == u'摄影作品':
            return
        second_cate_item = SheyingCateItem()
        for block in sel.css('div.node'):
            second_cate_item['name'] = block.xpath('div[@class="title"]/a/text()').extract()[0]
            second_cate_item['link'] = block.xpath('div[@class="title"]/a/@href').extract()[0]
            second_cate_item['level'] = '2'
            second_cate_item['up_level'] = first_cate
            yield second_cate_item
            url = second_cate_item['link']
            name = second_cate_item['name']
            yield Request(url, callback=self.get_second_cate,
                          meta={'first_cate': first_cate, 'second_cate': name})

    def get_article(self, response):
        first_cate = response.meta['first_cate']
        second_cate = response.meta['second_cate']
        article_item = SheyingArticleItem()
        sel = Selector(response)
        article_item['title'] = sel.css('div.title').xpath('h1/text()').extract_first()
        info = sel.css('div.info').xpath('span/text()').extract()
        article_item['author'] = None
        article_item['post_time'] = None
        if len(info) == 1:
            if is_valid_date(info[0]):
                article_item['post_time'] = info[0]
            else:
                article_item['author'] = info[0]
        else:
            article_item['author'] = info[0]
            article_item['post_time'] = info[-1]
        article_item['content'] = sel.xpath('//div[@class="area"]').extract_first()
        article_item['first_cate'] = first_cate
        article_item['second_cate'] = second_cate
        yield article_item
        url = sel.xpath('//span[@class="next"]/a/@href').extract()[0]
        a = 1
        yield Request(url, callback=self.get_article,
                      meta={'first_cate': first_cate, 'second_cate': second_cate})


def is_valid_date(str):
    """判断是否是一个有效的日期字符串"""
    try:
        time.strptime(str, "%Y-%m-%d")
        return True
    except:
        return False
