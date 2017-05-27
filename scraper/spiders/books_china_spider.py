# coding=utf-8
from __future__ import unicode_literals

import datetime

import scrapy
from mongoengine import NotUniqueError
from mongoengine import connect

from yuntu.documents import Book, BookCategory, BookUrl


class BooksChinaSpider(scrapy.Spider):
    # 定义爬虫的名称
    name = "books_china_spider"

    def __init__(self, **kwargs):
        super(BooksChinaSpider, self).__init__(**kwargs)
        connect('django')

    def start_requests(self):
        for cate in BookCategory.objects(level=1, crawled=False):
            url = cate.url[:-1]
            url += '_5_1_{}/'.format(cate.page)
            yield scrapy.Request(url=url, callback=self.parse_cate1, meta={'cate1': cate.code})
        for book_url in BookUrl.objects(crawled=False):
            yield scrapy.Request(url=book_url.url, callback=self.parse_page)

    def parse_cate1(self, response):
        for detail in response.xpath('//a[@class="titlein"]/@href').extract():
            url = 'http://www.bookschina.com' + detail
            try:
                BookUrl(url=url).save()
                print url
            except NotUniqueError:
                print url, '已存在'
        cate1 = BookCategory.objects(code=response.meta['cate1']).first()
        cate1.update(page=cate1.page + 1)
        next_url = response.xpath('//a[@class="nextPage"]/@href').extract_first()
        if next_url:
            next_url = 'http://www.bookschina.com' + next_url
            yield scrapy.Request(next_url, callback=self.parse_cate1, meta=response.meta)
        else:
            cate1 = BookCategory.objects(code=response.meta['cate1']).first()
            cate1.update(crawled=True)

    def parse_page(self, response):
        book = dict()
        book["source"] = 'bookschina'  # 来源
        book["title"] = response.xpath('//h1/text()').extract_first()
        book["url"] = response.url
        count = len(response.xpath('//div[@class="book_infor"]/p').extract())
        author = response.xpath('//div[@class="book_infor"]/p[1]/a/text()').extract_first()
        if author:
            book["author"] = author
        publisher = response.xpath('//div[@class="book_infor"]/p[2]/a/text()').extract_first()
        if publisher:
            book["publisher"] = publisher
        series = response.xpath('//div[@class="book_infor"]/p[3]/a/text()').extract_first()
        if series:
            book["series"] = series
        isbn = response.xpath('//div[@class="book_infor"]/p[{}]/i/text()'.format(count - 2)).extract_first()
        if isbn and isbn.split():
            book["isbn"] = isbn.split()[0]
        size = response.xpath('//div[@class="book_infor"]/p[{}]/i[1]/text()'.format(count - 1)).extract_first()
        if size and size.split():
            book["size"] = size.split()[0]
        page_number = response.xpath('//div[@class="book_infor"]/p[{}]/i[2]/text()'.format(count - 1)).extract_first()
        if page_number and page_number.split():
            page_number = page_number.split()[0]
            if page_number.isdigit():
                book["page_number"] = int(page_number)
        price = response.xpath('//div[@class="book_infor"]/p[{}]/i/text()'.format(count)).extract_first()
        if price and price.split():
            book["price"] = price.split()[0]
        time = response.xpath('//div[@class="book_infor"]/p[{}]/i[2]/text()'.format(count - 2)).extract_first()
        if time and time.split():
            time = time.split('/')
            book["publication_date"] = datetime.date(int(time[0]), int(time[1]), int(time[2]))
        cover = response.xpath('//div[@class="this_book_cover"]/img/@src').extract_first()
        if not cover:
            return
        if not cover.startswith('http'):
            cover = 'http://www.bookschina.com' + cover
        book["cover"] = cover
        book["cate1"] = response.xpath('//div[@class="this_crumb"]/a[2]/@href').extract_first().strip().split('/')[2][:4]
        cate2 = response.xpath('//div[@class="this_crumb"]/a[3]/@href').extract_first()
        if cate2:
            book["cate2"] = cate2.strip().split('/')[2][:4]
        summary = response.xpath('//h2[@id="this_intro"]/following-sibling::p/text()').extract_first()
        if summary:
            book["summary"] = summary
        catalog = response.xpath('//h2[@id="this_contents"]/following-sibling::p/text()').extract()
        if catalog:
            book["catalog"] = '\n'.join(catalog)
        url = BookUrl.objects(url=response.url).first()
        try:
            url.update(crawled=True)
        except:
            print '设置', response.url, 'crawled=True 失败'
        # for key in book:
        #     print key, book[key]
        try:
            Book(**book).save()
            print book['title'], book['url']
        except NotUniqueError:
            print book['url'], '已存在'
