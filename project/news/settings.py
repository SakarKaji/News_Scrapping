import logging

BOT_NAME = "news"

SPIDER_MODULES = ["news.spiders"]
NEWSPIDER_MODULE = "news.spiders"

logging.getLogger('scrapy').propagate = False
