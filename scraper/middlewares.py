# coding=utf-8
import random

from scrapy.exceptions import IgnoreRequest


class RandomUserAgent(object):
    """
    Randomly rotate user agents based on a list of predefined ones
    主要用来动态获取user agent, user agent列表USER_AGENTS在setting.py中进行配置
    """

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.agents))


class DownloaderMiddleware(object):
    @staticmethod
    def process_request(request, spider):
        if "turn" in request.meta:
            turn = request.meta["turn"]
            if turn != spider.turn:
                spider.logger.warning("in middleware, " + request.url + (" expire. %d %d" % (spider.turn, turn)))
                raise IgnoreRequest()
            else:
                return None
        else:
            return None
