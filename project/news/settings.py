import logging

BOT_NAME = "news"

SPIDER_MODULES = ["news.spiders"]
NEWSPIDER_MODULE = "news.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
PLAYWRIGHT_BROWSER_TYPE = "chromium" # or firefox
PLAYWRIGHT_LAUNCH_OPTIONS = {

    "headless": True,
    "timeout": 20 * 1000,  # 20 seconds
}
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 60 * 1000  # 10 seconds - page load timeout

logging.getLogger('scrapy').propagate = False