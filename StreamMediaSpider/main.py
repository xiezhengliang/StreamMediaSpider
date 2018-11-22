from scrapy import cmdline
from scrapy.http import Request
import requests
import json
if __name__ == '__main__':
    # cmdline.execute("scrapy crawl toutiao_app".split())
    # cmdline.execute("scrapy crawl toutiao_app_hot".split())
    # cmdline.execute("scrapy crawl souhu_app".split())
    cmdline.execute("scrapy crawl sina_app".split())
    # cmdline.execute("scrapy crawl tengxunxinwen_app".split())
    # cmdline.execute("scrapy crawl toutiaoxinwen_app".split())
    # cmdline.execute("scrapy crawl fenghuang_app".split())
    # cmdline.execute("scrapy crawl qutoutiao_app".split())
    # cmdline.execute("scrapy crawl wangyi_app".split())
    # cmdline.execute("scrapy crawl xinxileida".split())


