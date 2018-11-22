import scrapy
from StreamMediaSpider.items import SinaAppItem
import json
from StreamMediaSpider.tools import check_json_format
import configparser
import os
from StreamMediaSpider.para.parameter import Parameter
from os import path
from scrapy.http import Request

spder_db_name = "sina_parameter"
scrawl_urls = Parameter.get_sina_para(spder_db_name=spder_db_name)


class sina_app(scrapy.Spider):
    config = configparser.ConfigParser()
    # 获取当前目录
    d = path.dirname(__file__)
    # 获取当前目录的父级目录
    parent_path = os.path.dirname(d)
    logs_path = os.path.dirname(parent_path)
    custom_settings = {
        # 'LOG_FILE': logs_path+'/logs/sina_log.log',
        'DOWNLOAD_DELAY': 3,
        'DOWNLOAD_TIMEOUT': 5,
        'RETRY_TIMES': 3,
        'ITEM_PIPELINES': {
            'StreamMediaSpider.pipelines.SinaAppPipeline': 300,
        }
    }
    name = "wangyi_app"

    def start_requests(self):
        while scrawl_urls.__len__():
            par_tup = scrawl_urls.pop()
            formdata = {'version': '11.1.3', 'is_test': 'false', 'urs': '', 'store': '',
                        'ext_param': '''{"is_start": "0", "toppost": "1"}''',
                        'device': '''{"os": "android", "imei": "861980036599000",
                                   "device_id": "CQllNzU3MjVlM2I1YzNiZTc2CTU5ZTZiOGVj", "mac": "74:23:44:4E:C5:9C",
                                   "udid": "6d846390061a7498fa6dbafe35bf5693328903b2", "network_status": "wifi",
                                   "dq": "1920:1080", "isp": "", "dt": "Redmi Note 3", "mcc": "",
                                   "longitude": "113.381256", "latitude": "23.124437", "location_type": "1",
                                   "city_code": "440106"}''',
                        'adunit': '''{"category": "FOCUS2", "location": "1,2,10,20,21,22,23,24,25,26,27,28,29,30,31",
                                   "app": "7A16FBB6", "app_version": "43.1", "province": "%E5%B9%BF%E4%B8%9C",
                                   "city": "%E5%B9%BF%E5%B7%9E", "blacklist": ""}'''
                        }
            print(type(formdata))
            header = '''{'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Redmi Note 3 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 Mobile Safari/537.36',
                       ' Host': 'nex.163.com',
                       'Connection': 'Keep-Alive',
                       'Content-Type': 'application/json',
                       'Content-Length': '0',
                       'Cache-Control': 'no-cache'
            }'''
            yield scrapy.FormRequest(url="https://nex.163.com/q", headers=eval(header), formdata=formdata,
                                     callback=self.parse1)

    def parse1(self, response):
        if check_json_format(response.body.decode("utf-8")):
            pass
            # yield item
        back_url = response.meta['url']
        back_id = str(response.meta['id'])
        back_header = str(response.meta['header'])
        yield scrapy.Request(
            url=back_url, headers=eval(back_header), callback=self.parse1, priority=0, dont_filter=True,
            meta={'dont_redirect': True, 'id': back_id, 'header': back_header,
                  'url': back_url, 'handle_httpstatus_list': [302, 404, 403, 407, 500, 502, 503, 504, 408, 416, 400]})
#
