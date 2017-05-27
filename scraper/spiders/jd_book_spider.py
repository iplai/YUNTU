# coding=utf-8
from __future__ import unicode_literals

import datetime

import scrapy
from mongoengine import NotUniqueError
from mongoengine import connect

from yuntu.documents import Book, BookCategory


class JDSpider(scrapy.Spider):
    # 定义爬虫的名称
    name = "jd_book_spider"
    # 定义允许抓取的域名,如果不是在此列表的域名则放弃抓取
    # allowed_domains = ["jd.com"]
    # 定义抓取的入口url
    # start_urls = ["https://list.jd.com/list.html?cat=1713,3287,3797&page=1"]
    cate_url_format = 'https://list.jd.com/list.html?cat=1713,{cate1},{cate2}&page={page}&sort=sort_rank_asc&trans=1&JL=6_0_0#J_main'

    def __init__(self, **kwargs):
        super(JDSpider, self).__init__(**kwargs)
        connect('django')

    def start_requests(self):
        page = 5
        for cate1 in BookCategory.objects(level=1):
            for cate2 in cate1.children:
                yield scrapy.Request(
                    url=self.cate_url_format.format(cate1=cate1.code, cate2=cate2, page=page),
                    callback=self.parse,
                    meta={
                        "cate1": cate1.code,
                        "cate2": cate2,
                        "page": page,
                        'dont_redirect': True,
                        'handle_httpstatus_list': [302]
                    })

    def parse(self, response):
        bases = response.xpath('//li[@class="gl-item"]')
        for base in bases:
            cover = base.xpath(
                'descendant::div[@class="p-img"]/a/img/@data-lazy-img|descendant::div[@class="p-img"]/a/img/@src') \
                .extract_first()
            url = base.xpath('descendant::div[@class="p-img"]/a/@href').extract_first()
            # 获取书名，处理中文乱码
            title = base.xpath('descendant::div[@class="p-name"]/a/em/text()').extract_first().encode('utf-8', 'ignore')
            cover = 'http:' + cover
            url = 'http:' + url
            yield scrapy.Request(url, callback=self.parse_page, meta=dict(response.meta, cover=cover, title=title))
        # self.page_index += 1
        # new_url = response.url.split('page=')[0] + 'page=' + page
        # if self.page_index <= 247:
        #     yield scrapy.Request(new_url, callback=self.parse)
        response.meta["page"] += 1
        new_url = self.cate_url_format.format(**response.meta)
        yield scrapy.Request(new_url, callback=self.parse, meta=response.meta)

    def parse_page(self, response):
        # authors = response.xpath('//div[@class="p-author"]/a/text()').extract()
        authors = ''
        nodes = response.xpath('//div[@class="p-author"]/node()')  # node()匹配一个文本或者一个子节点
        for node in nodes:
            child_node = node.xpath('text()')
            if child_node:  # 或者是一个空list，或者是一个SelectorList，可以改成递归方法
                authors += child_node.extract_first().strip()
            else:
                authors += node.extract().strip()
        parameter_nodes = response.xpath('//ul[@class="p-parameter-list"]/li/node()')
        book = dict()
        book["jd_title"] = response.meta['title']
        book["url"] = response.url
        book["author"] = authors
        book["cover"] = response.meta['cover']
        book['cate1'] = BookCategory.objects(code=response.meta['cate1']).first()
        book['cate2'] = BookCategory.objects(code=response.meta['cate2']).first()
        items = ''
        for parameter_node in parameter_nodes:
            child_node = parameter_node.xpath('text()')
            if child_node:  # 或者是一个空list，或者是一个SelectorList，可以改成递归方法
                items += child_node.extract_first().strip()
                items += '|'
            else:
                key = parameter_node.extract().strip()
                # if key in ['出版社']
                items += key
                if key not in ['出版社：', '品牌：', '外文名称：', '丛书名：', '']:
                    items += '|'
        # print items
        for parameter in items.split('|')[:-1]:
            if parameter.startswith('出版社'):
                book["publisher"] = parameter.split('：')[1]
            if parameter.startswith('丛书'):
                book["series"] = parameter.split('：')[1]
            if parameter.startswith('外文名称'):
                book["foreign_title"] = parameter.split('：')[1]
            if parameter.startswith('ISBN'):
                book["isbn"] = parameter.split('：')[1]
            if parameter.startswith('出版时间'):
                time = parameter.split('：')[1].split('-')
                book["publication_date"] = datetime.date(int(time[0]), int(time[1]), int(time[2]))
            if parameter.startswith('包装'):
                book["package"] = parameter.split('：')[1]
            if parameter.startswith('附件：'):
                book["attachment"] = parameter.split('：')[1]
            if parameter.startswith('版次'):
                book["edition"] = int(parameter.split('：')[1])
            if parameter.startswith('用纸'):
                book["paper_type"] = parameter.split('：')[1]
            if parameter.startswith('正文语种'):
                book["language"] = parameter.split('：')[1]
            if parameter.startswith('开本'):
                book["size"] = parameter.split('：')[1]
            if parameter.startswith('页数'):
                page_number = parameter.split('：')[1]
                if page_number[-1] == 'p':
                    page_number = page_number[:-1]
                if page_number.isdigit():
                    book["page_number"] = int(page_number)
            if parameter.startswith('字数'):
                character_number = parameter.split('：')[1]
                if character_number.isdigit():
                    book["character_number"] = long(character_number)
        # book["summary"] = response.xpath('//div[@text="内容简介"]/div[1]/div/text()').extract_first()
        try:
            Book(**book).save()
            print book['jd_title'], book['url']
        except NotUniqueError:
            print book['url'], '已存在'
