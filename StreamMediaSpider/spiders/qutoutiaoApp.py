import scrapy
from StreamMediaSpider.items import SinaAppItem
import json
from StreamMediaSpider.tools import check_json_format
import configparser
import os
from StreamMediaSpider.para.parameter import Parameter
from os import path
from scrapy.http import Request

"""趣头条app爬虫"""

spder_db_name = "qutoutiao_parameter"
scrawl_urls = Parameter.get_qutoutiao_para(spder_db_name=spder_db_name)


class sina_app(scrapy.Spider):
    config = configparser.ConfigParser()
    # 获取当前目录
    d = path.dirname(__file__)
    # 获取当前目录的父级目录
    parent_path = os.path.dirname(d)
    logs_path = os.path.dirname(parent_path)
    custom_settings = {
        # 'LOG_FILE': logs_path+'/logs/sina_log.log',
        # 'DOWNLOAD_DELAY': 3,
        # 'DOWNLOAD_TIMEOUT': 5,
        # 'RETRY_TIMES': 3,
        'ITEM_PIPELINES': {
            'StreamMediaSpider.pipelines.QutoutiaoAppPipeline': 300,
        }
    }
    name = "qutoutiao_app"

    def start_requests(self):
        while scrawl_urls.__len__():
            par_tup = scrawl_urls.pop()
            formdata = {
                'media': '''{"type":1,"app":{"package_name":"com.jifen.qukan","app_version":"3.3.5.000.0915.1659","sdk_version":"1.655"},"browser":{"user_agent":"Dalvik\/2.1.0 (Linux; U; Android 6.0.1; Redmi Note 3 MIUI\/V8.5.3.0.MHOCNED)"},"support_feature":[1,5,6]}''',
                'client': '''{"type":1,"client_version":"1.6.0","version":"1.655.0.997"}''',
                'device': '''{"id_androidid":"e75725e3b5c3be76","height":1920,"width":1080,"brand":"Xiaomi","model":"Redmi Note 3","os_version":"6.0.1","os_type":1,"id_tkid":"RCLKXJkA5U6TgqvcCrqmzask","id_imei":"861980036599000"}''',
                'network': '''{"type":1}''',
                'adslot': '''{"id":"1026437","type":1,"height":100,"width":200,"channel":"255","memberid":"","qk_dtu_id":"002","req_id":"734ebf18c097c4943112d46cf030d7796fd0","total_req":19,"adslot_req":3}'''}
            yield scrapy.FormRequest(url=par_tup[2], headers=eval(par_tup[1]), formdata=formdata,
                                     callback=self.parse1)

    def parse1(self, response):
        html = response.body.text()
        if check_json_format(response.body.decode("utf-8")):
            jsonresponse = json.loads(response.body.decode("utf-8"))
            # print(type(jsonresponse))
            data = jsonresponse['data']
            if 'ad' in data:
                ad = data['ad']
                feed = ad['feed']
                for n in feed:
                    item = SinaAppItem()
                    item['pos'] = str(n.get('pos', ""))
                    item['newsId'] = str(n.get('newsId', ""))
                    item['title'] = str(n.get('title', ""))
                    item['link'] = str(n.get('link', ""))
                    item['pic'] = str(n.get('pic', ""))
                    item['showTag'] = str(n.get('showTag', ""))
                    item['articlePreload'] = str(n.get('articlePreload', ""))
                    if 'commentStatus' in n:
                        item['commentStatus'] = str(n['commentCountInfo']['commentStatus'])
                    else:
                        item['commentStatus'] = ''
                    item['adid'] = str(n.get('adid', ""))
                    item['dislikeTags'] = str(n.get('dislikeTags', ""))
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
