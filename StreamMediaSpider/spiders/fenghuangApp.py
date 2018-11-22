import scrapy
from StreamMediaSpider.tools import check_json_format
import json
import configparser
import os
from os import path
from StreamMediaSpider.para.parameter import Parameter
from scrapy.http import Request
from StreamMediaSpider.items import FenghuangAppItem

spder_db_name = "fenghuang_parameter"
scrawl_urls = Parameter.get_fenghuang_para(spder_db_name=spder_db_name)


class toutiao_app(scrapy.Spider):
    config = configparser.ConfigParser()
    # 获取当前目录
    d = path.dirname(__file__)
    # 获取当前目录的父级目录
    parent_path = os.path.dirname(d)
    logs_path = os.path.dirname(parent_path)
    custom_settings = {
        'LOG_FILE': logs_path + '/logs/fenghuang_log.log',
        # 'DOWNLOAD_DELAY': 2,
        'DOWNLOAD_TIMEOUT': 5,
        'RETRY_TIMES': 3,
        # 'LOG_LEVEL': 'DEBUG',
        'ITEM_PIPELINES': {
            'StreamMediaSpider.pipelines.FenghuangAppPipeline': 300,
        }
    }
    name = "fenghuang_app"

    def start_requests(self):
        while scrawl_urls.__len__():
            par_tup = scrawl_urls.pop()
            yield Request(url=par_tup[2], meta={'id': par_tup[0], 'header': par_tup[1], 'url': par_tup[2]},
                          callback=self.parse)

    def parse(self, response):
        if check_json_format(response.body.decode("utf-8", "ignore")):
            jsonresponse = json.loads(response.body.decode("utf-8", "ignore"))
            item_list = jsonresponse[0]["item"]
            for advert in item_list:
                if "style" in advert:
                    if "attribute" in advert["style"]:
                        if "广告" in advert["style"]["attribute"]:
                            item = FenghuangAppItem()
                            item['thumbnail'] = str(advert["thumbnail"])
                            item['title'] = str(advert["title"])
                            item['appSource'] = str(advert["appSource"])
                            item['intro'] = str(advert["intro"])
                            item['adId'] = str(advert["adId"])
                            item['adPositionId'] = str(advert["adPositionId"])
                            item['type'] = str(advert["type"])
                            item['source'] = str(advert["source"])
                            item['weburl'] = str(advert["link"].get("weburl", ""))
                            item['view'] = str(advert["style"].get("view", ""))
                            item['images'] = str(advert["style"].get("images", ""))
                            item['parameter_id'] = str(response.meta['id'])
                            yield item
        back_url = response.meta['url']
        back_id = str(response.meta['id'])
        back_header = str(response.meta['header'])
        yield scrapy.Request(
            url=back_url,  callback=self.parse, priority=0, dont_filter=True,
            meta={'dont_redirect': True, 'id': back_id, 'header': back_header,
                  'url': back_url, 'handle_httpstatus_list': [302, 404, 403, 407, 500, 502, 503, 504, 408, 416, 400]})
