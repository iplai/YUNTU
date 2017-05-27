# coding=utf-8
import json
import scrapy


class YuntuSpider(scrapy.Spider):
    # 定义爬虫的名称
    name = "yuntu_spider"

    def start_requests(self):
        cookies = {
            'JSESSIONID': '6C78D51424D94E6C523063294AF1596A'
        }
        return [scrapy.Request('http://adminx.libtop.com/library/show/' + str(i), cookies=cookies,
                               callback=self.parse_library)
                for i in range(1, 1000)]
        # return [scrapy.Request('http://adminx.libtop.com/opac/show/' + str(i), cookies=cookies,
        #                        callback=self.parse_opac)
        #         for i in range(1, 48)]
        # return [scrapy.Request('http://adminx.libtop.com/server/edit?id=' + str(i), cookies=cookies,
        #                        callback=self.parse_node)
        #         for i in range(1, 75)]

    def parse_library(self, response):
        item = {
            'id': response.xpath('//*[@id="libraryId"]/@value').extract_first().encode('utf-8'),
            'name': response.xpath('//*[@id="libraryName"]/@value').extract_first().encode('utf-8'),
            'province': response.xpath('//*[@id="provinceName"]/@value').extract_first().encode('utf-8'),
            'status': response.xpath('//*[@id="statusDesc"]/@value').extract_first().encode('utf-8'),
            'node_server': response.xpath('//*[@id="serverCode"]/@value').extract_first().encode('utf-8'),
            'node_ip': response.xpath('//*[@id="mirrored_IP"]/@value').extract_first().encode('utf-8'),
            'client_ip': response.xpath('//textarea[@id="client_IP"]/text()').extract_first().strip().encode('utf-8'),
            'opac_version': response.xpath('//*[@id="opacSystem"]/@value').extract_first().encode('utf-8'),
            'start_date': response.xpath('//*[@id="starttime"]/@value').extract_first().encode('utf-8'),
            'opac_url': response.xpath('//*[@id="url"]/@value').extract_first().encode('utf-8'),
            'remarks': response.xpath('//textarea[@id="remarks"]/text()').extract_first().strip().encode('utf-8'),
        }
        if item['id'] == '':
            return
        with open('static/tem/libraries.txt', 'a') as f:
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')

    def parse_node(self, response):
        item = {
            'name': response.xpath('//*[@id="code"]/@value').extract_first(),
            'library': response.xpath('//*[@name="deployment_school"]/@value').extract_first(),
            'deploy_date': response.xpath('//*[@name="deployment_date"]/@value').extract_first(),
            'level': response.xpath('//*[@id="node_level"]/option[@selected]/text()').extract_first(),
            'mirror_ip': response.xpath('//*[@name="mirror_ip"]/@value').extract_first(),
            'server_ip': response.xpath('//*[@name="svr_ip"]/@value').extract_first(),
            'netmask': response.xpath('//*[@name="netmask"]/@value').extract_first(),
            'gateway': response.xpath('//*[@name="gateway"]/@value').extract_first(),
            'public_ip': response.xpath('//*[@name="public_ip"]/@value').extract_first(),
            'dns': response.xpath('//*[@name="dns"]/@value').extract_first(),
            'os': response.xpath('//*[@name="os"]/@value').extract_first(),
            'ownership': response.xpath('//*[@id="ownership"]/option[@selected]/text()').extract_first(),
            'nic_bond': response.xpath('//*[@id="nic_bond"]/option[@selected]/text()').extract_first(),
            'hardware': response.xpath('//textarea[@id="hardinfo"]/text()').extract_first(),
            'ssh': response.xpath('//textarea[@id="client_IP"]/text()').extract_first(),
            'remarks': response.xpath('//textarea[@id="remark"]/text()').extract_first(),
        }
        result = {k: v.encode('utf-8') if v else '' for k, v in item.items()}

        with open('static/tem/node_servers.txt', 'a') as f:
            json.dump(result, f, ensure_ascii=False)
            f.write('\n')

    def parse_opac(self, response):
        item = {
            'name': response.xpath('//*[@id="opacName"]/@value').extract_first().encode('utf-8'),
            'version': response.xpath('//*[@id="version"]/@value').extract_first().encode('utf-8'),
            'alias': response.xpath('//*[@id="alias"]/@value').extract_first().encode('utf-8'),
        }
        if item['name'] == '':
            return
        with open('static/tem/opac.txt', 'a') as f:
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')

    def post_login(self, response):
        pass
