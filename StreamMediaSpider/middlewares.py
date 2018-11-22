# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
import requests
import json
import time
from StreamMediaSpider import userAgent
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import configparser
from os import path


class StreammediaspiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# UserAgent轮转
class userAgentDownloadMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        # ua = random.choice(self.user_agent_list)
        # if spider.name == 'toutiao':
        #     self.user_agent = random.choice(userAgent.user_agent_list)
        # elif spider.name == 'toutiao_app':
        self.user_agent = random.choice(userAgent.user_agent_mobile_list)
        print("userAgent:" + self.user_agent)
        request.headers.setdefault("User-Agent", self.user_agent)


class ProxyMiddleware():
    # json syntax ip,port,source
    def __init__(self):
        config = configparser.ConfigParser()
        # 获取当前目录
        d = path.dirname(__file__)
        config.read(d + "/config/config.ini")
        # 初始化数据库连接
        IPProxy_host = config.get("IPProxy", "host")
        IPProxy_port = config.get("IPProxy", "port")
        # r = requests.get("http://"+str(IPProxy_host)+":"+str(IPProxy_port)+"/?country=%s&type=0" % "国内")
        r = requests.get(
            "http://pool.ipproxy.nisure.cn/ipproxy_pool/for_scrapy/py/?types=0&count=10&country=国内")
        self.ip_ports = json.loads(r.text)
        self.num = 0
        self.max = 10

    def process_response(self, request, response, spider):
        '''对返回的response处理'''
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200:
            time.sleep(1)
            iport = random.choice(self.ip_ports)
            ip = iport[0]
            port = iport[1]
            cur_proxy = "http://" + ip + ":" + str(port)
            # print("this is response ip:"+cur_proxy)
            # 对当前reque加上代理
            request.meta['proxy'] = cur_proxy
            return request
        return response

    def process_request(self, request, spider):
        #         if self.num == 0:
        iport = random.choice(self.ip_ports)
        ip = iport[0]
        port = iport[1]
        self.cur_proxy = "http://" + ip + ":" + str(port)
        request.meta["proxy"] = self.cur_proxy
        # print(self.cur_proxy)

    def process_exception(self, request, exception, spider):
        # 出现异常时（超时）使用代理
        # print("\n出现异常，正在更新代理重试....\n")
        iport = random.choice(self.ip_ports)
        ip = iport[0]
        port = iport[1]
        cur_proxy = "http://" + ip + ":" + str(port)
        request.meta['proxy'] = cur_proxy
        return request
