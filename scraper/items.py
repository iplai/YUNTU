# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QiubaiScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    author = scrapy.Field()
    content = scrapy.Field()
    vote = scrapy.Field()
    comment = scrapy.Field()
    updated = scrapy.Field()


class CsdnblogItem(scrapy.Item):
    """存储提取信息数据结构"""

    title = scrapy.Field()
    link = scrapy.Field()
    description = scrapy.Field()
    post_date = scrapy.Field()
    view = scrapy.Field()


class TurnItem(scrapy.Item):
    id = scrapy.Field()
    mark = scrapy.Field()


class AgencyItem(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    county = scrapy.Field()
    address = scrapy.Field()
    name = scrapy.Field()
    windows = scrapy.Field()
    start = scrapy.Field()
    end = scrapy.Field()
    turn = scrapy.Field()


class StationItem(scrapy.Item):
    bureau = scrapy.Field()
    station = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    passenger = scrapy.Field()
    luggage = scrapy.Field()
    package = scrapy.Field()
    turn = scrapy.Field()


class BriefItem(scrapy.Item):
    code = scrapy.Field()
    train_no = scrapy.Field()
    start = scrapy.Field()
    end = scrapy.Field()
    turn = scrapy.Field()


class InfoItem(scrapy.Item):
    train_no = scrapy.Field()
    no = scrapy.Field()
    station = scrapy.Field()
    start_time = scrapy.Field()
    arrive_time = scrapy.Field()
    stopover_time = scrapy.Field()
    seat_type = scrapy.Field()
    turn = scrapy.Field()
    type = scrapy.Field()


class BriefDeltaItem(scrapy.Item):
    code = scrapy.Field()
    seat_type = scrapy.Field()
    turn = scrapy.Field()


class CodeItem(scrapy.Item):
    name = scrapy.Field()
    code = scrapy.Field()
    turn = scrapy.Field()


class TicketItem(scrapy.Item):
    train_no = scrapy.Field()
    start = scrapy.Field()
    end = scrapy.Field()
    swz = scrapy.Field()
    tz = scrapy.Field()
    zy = scrapy.Field()
    ze = scrapy.Field()
    gr = scrapy.Field()
    rw = scrapy.Field()
    yw = scrapy.Field()
    rz = scrapy.Field()
    yz = scrapy.Field()
    wz = scrapy.Field()
    qt = scrapy.Field()
    turn = scrapy.Field()


class SheyingArticleItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    post_time = scrapy.Field()
    first_cate = scrapy.Field()
    second_cate = scrapy.Field()


class SheyingCateItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    level = scrapy.Field()
    up_level = scrapy.Field()


"""
定义爬取古诗文网（gushiwen.org）的各数据项
时代：（先秦、唐、宋。。。）
作者
   风格
   作者介绍（名、字、生卒、画像。。。）
作品：
    作品正文、作品背景、后世评价、作品影响、其他名作
链接

"""


class GushiwenItem(scrapy.Item):
    PoetryLinks = scrapy.Field()
    # 处理具体作品
    PoetyName = scrapy.Field()
    PoetryDestiny = scrapy.Field()
    PoetryAuthor = scrapy.Field()
    PoetryPingfen = scrapy.Field()
    PoetryContent = scrapy.Field()
    # 处理参考翻译,使用嵌套
    Cankaofanyi = scrapy.Field()
    # 处理参考赏析，使用嵌套
    Cankaoshangxi = scrapy.Field()
    # 处理作者介绍，使用嵌套
    AuthorInstr = scrapy.Field()
