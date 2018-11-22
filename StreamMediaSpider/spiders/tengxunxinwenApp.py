import scrapy
from StreamMediaSpider.items import SinaAppItem
import json
from StreamMediaSpider.tools import check_json_format
import configparser
import os
from StreamMediaSpider.para.parameter import Parameter
from os import path
from scrapy.http import Request

spder_db_name = "tengxunxinwen_parameter"
scrawl_urls = Parameter.get_tengxunxinwen_para(spder_db_name=spder_db_name)


class sina_app(scrapy.Spider):
    config = configparser.ConfigParser()
    # 获取当前目录
    d = path.dirname(__file__)
    # 获取当前目录的父级目录
    parent_path = os.path.dirname(d)
    logs_path = os.path.dirname(parent_path)
    custom_settings = {
        'LOG_FILE': logs_path+'/logs/sina_log.log',
        'DOWNLOAD_DELAY': 3,
        'DOWNLOAD_TIMEOUT': 5,
        'RETRY_TIMES': 3,
        'ITEM_PIPELINES': {
            'StreamMediaSpider.pipelines.SinaAppPipeline': 300,
        }
    }
    name = "tengxunxinwen_app"

    def start_requests(self):
        while scrawl_urls.__len__():
            par_tup = scrawl_urls.pop()
            headers = eval(par_tup[1])
            yield Request(url=par_tup[2], meta={'id': par_tup[0], 'header': par_tup[1], 'url': par_tup[2]},
                          callback=self.parse1)

    def parse1(self, response):
        if check_json_format(response.body.decode("utf-8")):
            jsonresponse = json.loads(response.body.decode("utf-8"))
            print(type(jsonresponse))
        back_url = response.meta['url']
        back_id = str(response.meta['id'])
        back_header = str(response.meta['header'])
        yield scrapy.Request(
            url=back_url, headers=eval(back_header), callback=self.parse1, priority=0, dont_filter=True,
            meta={'dont_redirect': True, 'id': back_id, 'header': back_header,
                  'url': back_url, 'handle_httpstatus_list': [302, 404, 403, 407, 500, 502, 503, 504, 408, 416, 400]})
#
