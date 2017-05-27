# coding=utf-8
import scrapy
from scripts.yuntu_doc import *


# noinspection PyUnresolvedReferences
class CourseSpider(scrapy.Spider):
    # 定义爬虫的名称
    name = "course_spider"

    def __init__(self, **kwargs):
        super(CourseSpider, self).__init__(**kwargs)
        connect('django')
        self.count = 0

    def start_requests(self):
        for course in Course.objects:
            url = course.neteaseUrl2
            if not url:
                self.export_courses_error(course)
                continue
            yield scrapy.Request(url)

    def parse(self, response):
        pass

    def get_national_library_courses(self):
        # 国家图书馆公开课
        categories = {
            '哲学': 1, '宗教': 2, '社会学': 4, '民族与民俗学': 5, '政治学': 6, '法学': 7, '军事学': 8, '经济学': 9, '文化教育体育': 24,
            '信息管理学': 11, '语言文字学': 13, '文学': 14, '艺术学': 15, '史学': 16, '考古学': 25, '科学技术': 26,
        }
        for category in categories:
            url = 'http://open.nlc.cn/kvideo.php?do=search&labelid=' + str(categories[category])
            yield scrapy.Request(url, self.parse_nlc, meta={'category': category})

    def get_video_urls(self):
        for course in Course.objects(crawled=False):
            yield scrapy.Request(course.courseUrl, meta={'course': course}, callback=self.parse_course)

    def get_videos(self):
        for video in Video.objects(bigPicUrl=None):
            yield scrapy.Request(video.url, meta={'video': video}, callback=self.parse_video)

    def parse_course(self, response):
        self.count += 1
        playlist = response.xpath('//div[@id="j-playlist-container"]')
        urls = []
        if playlist:
            items = playlist.xpath('div[@class="listrow clear"]/div')
            for item in items:
                url = item.xpath('a/@href')
                url = url.extract_first() if url else response.url
                urls.append(url)
        else:
            urls.append(response.url)
        response.meta['course'].update(videoUrls=urls, crawled=True)
        print self.count,
        print urls

    def parse_nlc(self, response):
        items = response.xpath('//div[@class="courses"]/ul/li')
        f = open('scripts/nlc.txt', 'a')
        for item in items:
            cover = item.xpath('a/img/@src').extract_first()
            data = dict(
                title=item.xpath('a/p/text()').extract_first().encode('utf-8'),
                description=item.xpath('div/div[@class="course-intro"]/text()').extract_first().encode('utf-8'),
                cover=cover,
                kvideoid=item.xpath('a/@href').extract_first().split('/')[-1],
                classesid=re.search(r'MOOC(\d+)\.jpg', cover).group(1),
                category=response.meta['category']
            )
            json.dump(data, f, ensure_ascii=False)
            f.write('\n')

    def parse_netease_videos(self, response):
        # 网易云课堂
        items = response.xpath('//table[@id="list2"]/tr/td/a/@href').extract()
        response.meta['course'].update(videoUrls=items)

    def parse_video(self, response):
        title = response.xpath('//span[@class="f-fl f-thide sname"]/text()').extract_first()
        if not title:
            return  # 该视频正在翻译
        data = {}
        description = response.xpath('//div[@class="u-itrobox f-pa j-downitem"]/text()').extract_first()
        data['description'] = description
        flag = re.search(r'appsrc : \'(.*?)\',', response.text)
        videoUrl = flag.group(1) if flag else None
        videoUrl = videoUrl if len(videoUrl) > 0 else None
        if videoUrl:
            data['videoUrl'] = videoUrl
        cover = response.css('div.positem img::attr(src)').extract_first()
        data['bigPicUrl'] = cover
        data['crawled'] = True
        video = response.meta['video']
        video.update(**data)
        self.count += 1
        for i in data:
            print data[i]
        print self.count

        # def close(spider, reason):
        #     import codecs
        #     json.dump(spider.videos, codecs.open('videos.json', 'a', 'utf-8'), ensure_ascii=False, indent=4)
        #     print 'Saved!'
        #     super(CourseSpider, spider).close(spider, reason)
