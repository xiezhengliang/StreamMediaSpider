import scrapy
from StreamMediaSpider.items import SouhuAppItem
from StreamMediaSpider.tools import check_json_format
import json
import configparser
import os
from os import path
from StreamMediaSpider.para.parameter import Parameter
from scrapy.http import Request

spder_db_name = "souhu_parameter"
scrawl_urls = Parameter.get_souhu_para(spder_db_name=spder_db_name)
class toutiao_app(scrapy.Spider):
    config = configparser.ConfigParser()
    # 获取当前目录
    d = path.dirname(__file__)
    # 获取当前目录的父级目录
    parent_path = os.path.dirname(d)
    logs_path = os.path.dirname(parent_path)
    custom_settings = {
        # 'LOG_FILE': logs_path+'/logs/souhu_log.log',
        'DOWNLOAD_DELAY': 2,
        'DOWNLOAD_TIMEOUT': 5,
        'RETRY_TIMES': 3,
        'ITEM_PIPELINES': {
            'StreamMediaSpider.pipelines.SouhuAppPipeline': 300,
        }
    }
    name = "souhu_app"
    def start_requests(self):
        while scrawl_urls.__len__():
            par_tup = scrawl_urls.pop()
            yield Request(url=par_tup[2], meta={'id': par_tup[0], 'header': par_tup[1], 'url': par_tup[2]}, callback= self.parse)


    def parse(self, response):
        if check_json_format(response.body.decode("utf-8")):
            jsonresponse = json.loads(response.body.decode("utf-8"))
            if 'recommendArticles' in jsonresponse:
                news = jsonresponse['recommendArticles']
                for ad in news:
                    if 'iconText' in ad:
                        if '广告' == ad['iconText']:
                            item = SouhuAppItem()
                            data = ad['data']
                            if 'error' in data and '1' == str(data['error']):
                                pass
                            else:
                                item['monitorkey'] = str(data.get('monitorkey', ""))
                                item['resource'] = str(data.get('resource', ""))
                                item['resource2'] = str(data.get('resource2', ""))
                                item['weight'] = str(data.get('weight', ""))
                                item['itemspaceid'] = str(data.get('itemspaceid', ""))
                                item['resource1'] = str(data.get('resource1', ""))
                                item['impressionid'] = str(data.get('impressionid', ""))
                                item['special'] = str(data.get('special', ""))
                                item['offline'] = str(data.get('offline', ""))
                                item['adid'] = str(data.get('adid', ""))
                                item['viewmonitor'] = str(data.get('viewmonitor', ""))
                                item['size'] = str(data.get('size', ""))
                                item['online'] = str(data.get('online', ""))
                                item['position'] = str(data.get('position', ""))
                                item['tag'] = str(data.get('tag', ""))
                                item['editNews'] = str(ad.get('editNews', ""))
                                item['statsType'] = str(ad.get('statsType', ""))
                                item['isPreload'] = str(ad.get('isPreload', ""))
                                item['newsType'] = str(ad.get('newsType', ""))
                                item['gbcode'] = str(ad.get('gbcode', ""))
                                item['commentNum'] = str(ad.get('commentNum', ""))
                                item['isHasSponsorships'] = str(ad.get('isHasSponsorships', ""))
                                item['recomTime'] = str(ad.get('recomTime', ""))
                                item['newsId'] = str(ad.get('newsId', ""))
                                item['iconNight'] = str(ad.get('iconNight', ""))
                                item['isWeather'] = str(ad.get('isWeather', ""))
                                item['isRecom'] = str(ad.get('isRecom', ""))
                                item['iconText'] = str(ad.get('iconText', ""))
                                item['link'] = str(ad.get('link', ""))
                                item['iconDay'] = str(ad.get('iconDay', ""))
                                item['abposition'] = str(ad.get('abposition', ""))
                                item['adType'] = str(ad.get('adType', ""))
                                item['playTime'] = str(ad.get('playTime', ""))
                                item['adp_type'] = str(ad.get('adp_type', ""))
                                item['isFlash'] = str(ad.get('isFlash', ""))
                                item['isHasTv'] = str(ad.get('isHasTv', ""))
                                item['newschn'] = str(ad.get('newschn', ""))
                                item['parameter_id'] = str(response.meta['id'])
                                yield item
        back_url = response.meta['url']
        back_id = str(response.meta['id'])
        back_header = str(response.meta['header'])
        yield scrapy.Request(
            url=back_url, headers=eval(back_header), callback=self.parse, priority=0, dont_filter=True,
            meta={'dont_redirect': True, 'id': back_id, 'header': back_header,
                  'url': back_url, 'handle_httpstatus_list': [302, 404, 403, 407, 500, 502, 503, 504, 408, 416, 400]})
