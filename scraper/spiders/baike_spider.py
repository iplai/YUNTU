# coding=utf-8
import json
import scrapy


class BaikeSpider(scrapy.Spider):
    # 定义爬虫的名称
    name = "baike_spider"

    def start_requests(self):
        nations = [
            "汉族",
            "壮族",
            "满族",
            "回族",
            "苗族",
            "维吾尔族",
            "土家族",
            "彝族",
            "蒙古族",
            "藏族",
            "布依族",
            "侗族",
            "瑶族",
            "朝鲜族",
            "白族",
            "哈尼族",
            "哈萨克族",
            "黎族",
            "傣族",
            "畲族",
            "傈僳族",
            "仡佬族",
            "东乡族",
            "高山族",
            "拉祜族",
            "水族",
            "佤族",
            "纳西族",
            "羌族",
            "土族",
            "仫佬族",
            "锡伯族",
            "柯尔克孜族",
            "达斡尔族",
            "景颇族",
            "毛南族",
            "撒拉族",
            "布朗族",
            "塔吉克族",
            "阿昌族",
            "普米族",
            "鄂温克族",
            "怒族",
            "京族",
            "基诺族",
            "德昂族",
            "保安族",
            "俄罗斯族",
            "裕固族",
            "乌孜别克族",
            "门巴族",
            "鄂伦春族",
            "独龙族",
            "塔塔尔族",
            "赫哲族",
            "珞巴族"
        ]
        return [scrapy.Request('http://baike.baidu.com/item/' + nation,
                               meta={'dont_redirect': True, 'handle_httpstatus_list': [302]}) for nation in nations]

    def parse(self, response):
        with open('nations.txt', 'a') as f:
            items = response.css('dl.basicInfo-block > dt')
            for item in items:
                key = item.css('::text')
                value = ''
                if key: key = key.extract_first().strip()
                tem = item.xpath('following-sibling::dd[1]/descendant-or-self::*/text()')
                if tem:
                    for i in tem.extract():
                        value += i.strip()
                f.write(key.encode('utf-8') + ':' + value.encode('utf-8') + '\n')
            # f.write('简介:' + summary.encode('utf-8') + '\n')
