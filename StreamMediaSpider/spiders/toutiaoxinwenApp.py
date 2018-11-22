import scrapy
from scrapy.selector import Selector
import json
import configparser
import os
from StreamMediaSpider.para.parameter import Parameter
from os import path
from scrapy.http import Request
from StreamMediaSpider.items import ToutiaoxinwenAppItem

spder_db_name = "toutiaoxinwen_parameter"
scrawl_urls = Parameter.get_toutiaoxinwen_para(spder_db_name=spder_db_name)


class sina_app(scrapy.Spider):
    config = configparser.ConfigParser()
    # 获取当前目录
    d = path.dirname(__file__)
    # 获取当前目录的父级目录
    parent_path = os.path.dirname(d)
    logs_path = os.path.dirname(parent_path)
    custom_settings = {
        'LOG_FILE': logs_path+'/logs/toutiaoxinwen_log.log',
        'DOWNLOAD_DELAY': 3,
        'DOWNLOAD_TIMEOUT': 5,
        'RETRY_TIMES': 3,
        'ITEM_PIPELINES': {
            'StreamMediaSpider.pipelines.ToutiaoxinwenAppPipeline': 300,
        }
    }
    name = "toutiaoxinwen_app"

    def start_requests(self):
        while scrawl_urls.__len__():
            par_tup = scrawl_urls.pop()
            headers = eval(par_tup[1])
            url = par_tup[2]
            yield Request(url=par_tup[2], meta={'id': par_tup[0], 'header': par_tup[1], 'url': par_tup[2]},
                          headers=eval(par_tup[1]), callback=self.parse1)

    def parse1(self, response):
        html = response.body.decode("utf-8")
        n_item_ad = Selector(text=html).xpath("//div[@class='scroll-touch-layout']//li[@data-id='4395823']").extract()
        if n_item_ad:
            for ad in n_item_ad:
                item = ToutiaoxinwenAppItem()
                item['url'] = Selector(text=ad).xpath("//a/@href").extract()[0]
                item['data_description'] = Selector(text=ad).xpath("//a/@data-description").extract()[0]
                ad_id= Selector(text=ad).xpath("//a/@data-ad-id").extract()[0]
                item['ad_id'] = ad_id
                item['title'] = Selector(text=ad).xpath("//div[@class='n-title element']/span/text()").extract()[0]
                item['publisher'] = \
                Selector(text=ad).xpath("//div[@class='n-desc']//span[@class='n-publisher']/text()").extract()[0]
                item['img_url'] = str(Selector(text=ad).xpath(
                    "//div[@class='n-img-wrapper']//div[@class='content img-loaded']/img/@src").extract())
                item['parameter_id'] = str(response.meta['id'])
                yield item
        back_url = response.meta['url']
        back_id = str(response.meta['id'])
        back_header = str(response.meta['header'])
        yield scrapy.Request(
            url=back_url, headers=eval(back_header), callback=self.parse1, priority=0, dont_filter=True,
            meta={'dont_redirect': True, 'id': back_id, 'header': back_header,
                  'url': back_url, 'handle_httpstatus_list': [302, 404, 403, 407, 500, 502, 503, 504, 408, 416, 400]})
#
