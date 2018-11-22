import scrapy
from StreamMediaSpider.items import SinaAppItem
import json
from StreamMediaSpider.tools import check_json_format
import configparser
import os
from StreamMediaSpider.para.parameter import Parameter
from os import path
from scrapy.http import Request




class xinxileida_app(scrapy.Spider):
    # config = configparser.ConfigParser()
    # 获取当前目录
    # d = path.dirname(__file__)
    # 获取当前目录的父级目录
    # parent_path = os.path.dirname(d)
    # logs_path = os.path.dirname(parent_path)
    # custom_settings = {
        # 'LOG_FILE': logs_path+'/logs/sina_log.log',
        # 'DOWNLOAD_DELAY': 3,
        # 'DOWNLOAD_TIMEOUT': 5,
        # 'RETRY_TIMES': 3,
        # 'ITEM_PIPELINES': {
        #     'StreamMediaSpider.pipelines.SinaAppPipeline': 300,
        # }
    # }
    name = "xinxileida"

    def start_requests(self):
        loginForm = {
            "LoginForm[username]": 15986323409,
            "LoginForm[password]": 123456,
        }
        unicornHeader = {
            'Host': 'Host: www.ad1024.com',
            'Referer': 'Referer: http://www.ad1024.com/site/login?callback=%2Fsite%2Findex%3Fsite%252Findex%3D&showGrowl=1&new_address=1',
            'Content - Length': '66',
            'User - Agent': 'Mozilla / 5.0(Windows NT 6.3;WOW64;Trident / 7.0;rv: 11.0) likeGecko',
            'Accept - Language': 'zh - Hans - CN, zh - Hans;q = 0.8, en - US;q = 0.5, en;q = 0.3',
        }
        customerData = {'key1': 'value1'}
        yield scrapy.FormRequest(url="http://www.ad1024.com/site/login?callback=%2Fsite%2Findex%3Fsite%252Findex%3D&showGrowl=1&new_address=1",
                      headers=unicornHeader,
                      method='POST',  # GET or POST
                      formdata=loginForm,   # 表单提交的数据
                      meta=customerData,     # 自定义，向response传递数据
                      callback=self.parse1,
                      errback=self.error_handle,
                      # 如果需要多次提交表单，且url一样，那么就必须加此参数dont_filter，防止被当成重复网页过滤掉了
                      dont_filter=True)

    def parse1(self, response):
        print("parse1")
        text = response.body.text()
        yield scrapy.Request(
           )

    def error_handle(self, response):
        print("error_handle")
        text = response.body.text()
#
