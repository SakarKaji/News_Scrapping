import scrapy
from Utils import Utils
from Utils import PostNews
from Utils.Constants import Standard_Category
from datetime import datetime, timedelta
from news.article_object import article_data
import logging
import random

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0',
]

class EKantipurScraper(scrapy.Spider):
    name = "ekantipur"
    start_urls = ["https://ekantipur.com/"]

    custom_settings = {
        'LOG_LEVEL': logging.DEBUG,
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 1,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1,
        'AUTOTHROTTLE_MAX_DELAY': 60,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,
        'AUTOTHROTTLE_DEBUG': True,
    }

    def __init__(self):
        self.data = []
        self.articlelink_xpath = '//ul/li[@class="nav-item "]'
        self.title_xpath = '//div[contains(@class,"a-inner-header")]//h1/text()'
        self.datepath = "//div[contains(@class,'details-meta')]//span[@class='detail-date']/text()"
        self.datepath2 = '//span[@class="published-at"]/text()'
        self.description_xpath = "//div[contains(@class,'description')]//p/text()"
        self.link_xpath = "//article[@class='normal']/div[@class='teaser offset']/h2/a/@href"
        self.image_xpath = "//div[contains(@class,'image')]/figure/img/@src"
        self.today_date = datetime.today().strftime('%Y-%m-%d')
        self.article_source = "ekantipur"

    def start_requests(self):
        user_agent = random.choice(USER_AGENTS)
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers={'User-Agent': user_agent})

    def parse(self, response):
        user_agent = random.choice(USER_AGENTS)
        headers = {'User-Agent': user_agent}
        
        for link in response.xpath(self.articlelink_xpath):
            category = link.xpath(".//a/text()").get()
            category_link = link.xpath(".//a/@href").get()
            if category and category_link:
                yield scrapy.Request(
                    url=category_link,
                    callback=self.scrape_each_category,
                    errback=self.handle_failure,
                    headers=headers,
                    meta={"link": category_link, "category": category}
                )

    def handle_failure(self, failure):
        """
        Handle failure during request.
        """
        self.logger.error(f"Request failed: {failure.request.url}")

    def scrape_each_category(self, response):
        category = response.meta["category"]
        links = []

        if category == "अर्थ / वाणिज्य":
            links = response.xpath('(//div[@class="bazar-layout"]//article//figure//a[1]/@href)').getall()
            for link in links:
                if not link.startswith('https://'):
                    link = "https://ekantipur.com" + link
                yield scrapy.Request(
                    url=link,
                    callback=self.scrape_each_article,
                    headers={'User-Agent': random.choice(USER_AGENTS)},
                    meta={"link": link, "category": category}
                )

        links = response.xpath(self.link_xpath).getall()
        for link in links:
            link = "https://ekantipur.com" + link if not link.startswith('https://') else link
            yield scrapy.Request(
                url=link,
                callback=self.scrape_each_article,
                headers={'User-Agent': random.choice(USER_AGENTS)},
                meta={"link": link, "category": category}
            )

    def scrape_each_article(self, response):
        category = response.meta["category"]
        category_mapping = {
            "समाचार": Standard_Category.OTHERS,
            "अर्थ / वाणिज्य": Standard_Category.FINANCE,
            "विचार": Standard_Category.OPINION,
            "खेलकुद": Standard_Category.SPORTS,
            "उपत्यका": Standard_Category.OTHERS,
            "मनोरञ्जन": Standard_Category.ENTERTAINMENT,
            "फोटोफिचर": Standard_Category.OTHERS,
            "फिचर": Standard_Category.OTHERS,
            "विश्व": Standard_Category.INTERNATIONAL,
            "ब्लग": Standard_Category.OTHERS,
            "कोसेली": Standard_Category.OTHERS,
            "प्रवास": Standard_Category.TRAVEL,
            "शिक्षा": Standard_Category.EDUCATION,
        }
        category_name = category_mapping.get(category, Standard_Category.OTHERS)
        response.meta["category"] = category_name

        date = response.xpath(self.datepath).get() or response.xpath(self.datepath2).get()
        if date:
            self.formattedDate = Utils.ekantipur_conversion(date)
            five_days_ago = datetime.now() - timedelta(days=5)
            if self.formattedDate and datetime.strptime(self.formattedDate, "%Y-%m-%d") >= five_days_ago:
                news_obj = article_data(self, response)
                print(news_obj)
                PostNews.postnews(news_obj)
