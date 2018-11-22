# -*- coding: utf-8 -*-

# Scrapy settings for StreamMediaSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

# BOT_NAME = 'StreamMediaSpider'

SPIDER_MODULES = ['StreamMediaSpider.spiders']
NEWSPIDER_MODULE = 'StreamMediaSpider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'StreamMediaSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#设置下载的等待时间
# DOWNLOAD_DELAY = 2
# DOWNLOAD_TIMEOUT = 5
# RETRY_TIMES = 4

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

#CRITICAL - 严重错误(critical)
#ERROR - 一般错误(regular errors)
#WARNING - 警告信息(warning messages)
#INFO - 一般信息(informational messages)
#DEBUG - 调试信息(debugging messages)
LOG_LEVEL = 'INFO'
# LOG_FILE  ='../logs/default/toutiao_app/toutiao_log'
# Disable cookies (enabled by default)
COOKIES_ENABLED = False
# DOWNLOAD_FAIL_ON_DATALOSS = False
# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   'StreamMediaSpider.middlewares.StreammediaspiderSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'StreamMediaSpider.middlewares.userAgentDownloadMiddleware': 543,
    'StreamMediaSpider.middlewares.ProxyMiddleware': 100,
   #  'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware':500,
    # 'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware':None,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#     # 'StreamMediaSpider.pipelines.SinaAppPipeline': 300,
#     'StreamMediaSpider.pipelines.ToutiaoAppPipeline': 300,
#     'StreamMediaSpider.pipelines.SouhuAppPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
