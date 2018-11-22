import scrapy
from StreamMediaSpider.items import ToutiaoAppItem
from StreamMediaSpider.tools import check_json_format
import json
from scrapy.spider import CrawlSpider
import configparser
from StreamMediaSpider.para.parameter import Parameter
import os
from scrapy.http import Request
from os import path

spder_db_name = "toutiao_parameter"
scrawl_urls = Parameter.get_toutiao_para(spder_db_name=spder_db_name)
class toutiao_app(CrawlSpider):
    config = configparser.ConfigParser()
    # 获取当前目录
    d = path.dirname(__file__)
    # 获取当前目录的父级目录
    parent_path = os.path.dirname(d)
    logs_path = os.path.dirname(parent_path)
    custom_settings = {
        'LOG_FILE': logs_path + '/logs/toutiao_log.log',
        # 'COOKIES_ENABLED':'True',
        # 'DOWNLOAD_DELAY': 1,
        'DOWNLOAD_TIMEOUT': 3,
        'RETRY_TIMES': 1,
        'IMAGES_STORE': 'images',
        'IMAGES_STORE': 'image_urls',
        'ITEM_PIPELINES': {
            'StreamMediaSpider.pipelines.ToutiaoAppPipeline': 300,
        }
    }
    name = "toutiao_app"

    def start_requests(self):
        while scrawl_urls.__len__():
            par_tup = scrawl_urls.pop()
            yield Request(url=par_tup[2], meta={'id': par_tup[0], 'header': par_tup[1], 'url': par_tup[2]}, callback= self.parse)

    def parse(self, response):
        if check_json_format(response.body.decode("utf-8", "ignore")):
            jsonresponse = json.loads(response.body.decode("utf-8", "ignore"))
            news = jsonresponse['data']
            for n in news:
                dict_news = json.loads(n['content'])
                if 'label' in dict_news:
                    if '广告' in str(dict_news['label']):
                        item = ToutiaoAppItem()
                        item['abstract'] = str(dict_news.get('abstract', ""))
                        item['action_list'] = str(dict_news.get('action_list', ""))
                        item['aggr_type'] = str(dict_news.get('aggr_type', ""))
                        item['allow_download'] = str(dict_news.get('allow_download', ""))
                        item['article_sub_type'] = str(dict_news.get('article_sub_type', ""))
                        item['article_tpye'] = str(dict_news.get('article_tpye', ""))
                        item['article_url'] = str(dict_news.get('article_url', ""))
                        item['ban_comment'] = str(dict_news.get('ban_comment', ""))
                        item['behot_time'] = str(dict_news.get('behot_time', ""))
                        item['bury_count'] = str(dict_news.get('bury_count', ""))
                        item['cell_flag'] = str(dict_news.get('cell_flag', ""))
                        item['cell_layout_style'] = str(dict_news.get('cell_layout_style', ""))
                        item['cell_type'] = str(dict_news.get('cell_type', ""))
                        item['comment_count'] = str(dict_news.get('comment_count', ""))
                        item['content_decoration'] = dict_news.get('content_decoration', "")
                        item['digg_count'] = str(dict_news.get('digg_count', ""))
                        item['display_url'] = str(dict_news.get('display_url', ""))
                        item['filter_words'] = str(dict_news.get('filter_words', ""))
                        item['group_flags'] = str(dict_news.get('group_flags', ""))
                        item['has_video'] = str(dict_news.get('has_video', ""))
                        item['hot'] = str(dict_news.get('hot', ""))
                        item['ignore_web_transform'] = str(dict_news.get('ignore_web_transform', ""))
                        item['is_subject'] = str(dict_news.get('is_subject', ""))
                        item['item_id'] = str(dict_news.get('item_id', ""))
                        item['item_version'] = str(dict_news.get('item_version', ""))
                        item['label'] = str(dict_news.get('label', ""))
                        item['label_style'] = str(dict_news.get('label_style', ""))
                        item['large_image_list'] = str(dict_news.get('large_image_list', ""))
                        item['level'] = str(dict_news.get('level', ""))
                        item['log_pb'] = str(dict_news.get('log_pb', ""))
                        item['natant_level'] = str(dict_news.get('natant_level', ""))
                        item['preload_web'] = str(dict_news.get('preload_web', ""))
                        item['publish_time'] = str(dict_news.get('publish_time', ""))
                        item['raw_ad_data'] = str(dict_news.get('raw_ad_data', ""))
                        item['read_count'] = str(dict_news.get('read_count', ""))
                        item['repin_count'] = str(dict_news.get('repin_count', ""))
                        item['rid'] = str(dict_news.get('rid', ""))
                        item['share_count'] = str(dict_news.get('share_count', ""))
                        item['share_info'] = str(dict_news.get('share_info', ""))
                        item['share_url'] = str(dict_news.get('share_url', ""))
                        item['show_dislike'] = str(dict_news.get('show_dislike', ""))
                        item['show_portrait'] = str(dict_news.get('show_portrait', ""))
                        item['show_portrait_article'] = str(dict_news.get('show_portrait_article', ""))
                        item['source'] = str(dict_news.get('source', ""))
                        item['source_avatar'] = str(dict_news.get('source_avatar', ""))
                        item['tag'] = str(dict_news.get('tag', ""))
                        item['group_id'] = str(dict_news.get('group_id', ""))
                        item['tag_id'] = str(dict_news.get('tag_id', ""))
                        item['title'] = str(dict_news.get('title', ""))
                        item['url'] = str(dict_news.get('url', ""))
                        item['user_repin'] = str(dict_news.get('user_repin', ""))
                        item['user_verified'] = str(dict_news.get('user_verified', ""))
                        item['video_detail_info'] = str(dict_news.get('video_detail_info', ""))
                        item['video_duration'] = str(dict_news.get('video_duration', ""))
                        item['video_id'] = str(dict_news.get('video_id', ""))
                        item['video_play_info'] = str(dict_news.get('video_play_info', ""))
                        item['video_proportion_article'] = str(dict_news.get('video_proportion_article', ""))
                        item['video_style'] = str(dict_news.get('video_style', ""))
                        if 'large_image_list' in dict_news:
                            image_urls = eval(str(dict_news['large_image_list']))[0]['url']
                            item['image_urls'] = image_urls
                        item['parameter_id'] = response.meta['id']
                        yield item
        back_url = response.meta['url']
        back_id = str(response.meta['id'])
        back_header = str(response.meta['header'])
        yield scrapy.Request(
            url=back_url, headers=eval(back_header), callback=self.parse, priority=0, dont_filter=True,
            meta={'dont_redirect': True, 'id': back_id, 'header': back_header,
                  'url': back_url, 'handle_httpstatus_list': [302, 404, 403, 407, 500, 502, 503, 504, 408, 416, 400]})
