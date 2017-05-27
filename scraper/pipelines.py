# -*- coding: utf-8 -*-
from datetime import datetime

import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

from .items import SheyingCateItem, SheyingArticleItem


class QiubaiScrapyPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    # pipeline默认调用
    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self.insert_item, item, spider)
        d.addBoth(lambda _: item)
        return item

    # 将每行更新或写入数据库中
    def insert_item(self, conn, item, spider):
        # linkmd5id = self.get_url_md5(item)
        # print linkmd5id
        # print u'insert item---------------------\n'
        now = datetime.now().replace(microsecond=0).isoformat(' ')
        # conn.execute("""select 1 from cnblogsinfo where linkmd5id = %s""",
        #              (linkmd5id, ))
        # ret = conn.fetchone()
        #
        # if ret:
        #     conn.execute("""
        #     update cnblogsinfo set title = %s, description = %s, link = %s, listUrl = %s, updated = %s where linkmd5id = %s
        #     """, (item['title'], item['desc'], item['link'], item['listUrl'], now, linkmd5id))
        # else:
        #     conn.execute("""
        #     insert into cnblogsinfo(linkmd5id, title, description, link, listUrl, updated)
        #     values(%s, %s, %s, %s, %s, %s)
        #     """, (linkmd5id, item['title'], item['desc'], item['link'], item['listUrl'], now))
        conn.execute("""
        insert into qiushibaike(author, content, vote, comment, updated)
        values(%s, %s, %s, %s, %s)
        """, (item['author'], item['content'], item['vote'], item['comment'], now))


class CsdnblogPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    # pipeline默认调用
    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self.insert_item, item, spider)
        d.addBoth(lambda _: item)
        return 'pipeline end-------------------------'

    # 将每行更新或写入数据库中
    def insert_item(self, conn, item, spider):
        # 使用execute方法执行SQL语句
        conn.execute("""
        insert into csdn_blogs(title, link, description, post_date, view)
        values(%s, %s, %s, %s, %s)
        """, (item['title'], item['link'], item['description'], item['post_date'], item['view']))


class StationSQLPipeline(object):
    def __init__(self, dbpool):
        self.sql = '''
        INSERT INTO station(bureau, station, name, address, passenger, luggage, package)
        VALUES(%s, %s, %s, %s, %s, %s, %s)'''
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    # pipeline默认调用
    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self.insert_item, item, spider)
        d.addBoth(lambda _: item)
        return '-------------------end pipeline'

    # 将每行更新或写入数据库中
    def insert_item(self, conn, item, spider):
        # 使用execute方法执行SQL语句
        conn.execute(self.sql, (item["bureau"], item["station"],
                                item["name"], item["address"],
                                item["passenger"], item["luggage"],
                                item["package"]))


class SheyingPipeline(object):
    def __init__(self):
        self.cate_sql = "INSERT INTO `sheying_cate`(name,link,level,up_level) VALUES(%s, %s, %s, %s)"
        self.article_sql = "INSERT INTO `sheying_article`() VALUES(%s, %s, %s, %s, %s, %s)"
        self.db = MySQLdb.connect("localhost", "root", "", "django_db", charset='utf8')
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        try:
            if isinstance(item, SheyingCateItem):
                myitem=item
                self.cursor.execute(self.cate_sql, (item["name"],item["link"],
                                                    item["level"], item["up_level"]))
            elif isinstance(item, SheyingArticleItem):
                myitem=item
                self.cursor.execute(self.article_sql, (item["title"],item["author"],
                                                       item["content"], item["post_time"],
                                                       item["first_cate"], item["second_cate"]))
            self.db.commit()
        except Exception, e:
            spider.logger.warning("execute sql fail.")
            spider.logger.warning(str(e))
            self.db.rollback()
            # self.db.close()


class GushiwenPipeline(object):
    def process_item(self, item, spider):
        return item