import scrapy
from datetime import datetime, timedelta
from Utils import PostNews
from Utils.Constants import Standard_Category
from news.article_object import article_data


class bbcNepali_scrapper(scrapy.Spider):
    name = "bbcNepali"

    def __init__(self):
        self.articlelink_xpath = 'https://www.bbc.com/nepali'
        self.articles_xpath = '//div/div/section[1]/div/ul//h3[@class="bbc-1kr00f0 e47bds20"]/a/@href'
        self.description_xpath = '//*[@id="main-wrapper"]/div/div/div/div[1]/main/div/p/text()'
        self.title_xpath = '//*[@id="content"]/text()'
        self.image_xpath = '//div[@class="bbc-j1srjl"]/img/@src'
        self.date_xpath = '//div[@class="bbc-19j92fr ebmt73l0"]/time/@datetime'
        self.article_source = 'bbcnepali'

    def start_requests(self):
        yield scrapy.Request(url=self.articlelink_xpath, callback=self.parse)

    def parse(self, response):
        for link in response.xpath(self.articles_xpath).getall():
            print(f"Link :: {link}")
            yield scrapy.Request(url=link, callback=self.parse_article)

    def parse_article(self, response):
        self.formattedDate = response.xpath(self.date_xpath).get()
        response.meta['category'] = Standard_Category.OTHERS
        five_days_ago = datetime.now() - timedelta(days=5)
        if self.formattedDate and (datetime.strptime(self.formattedDate, "%Y-%m-%d") >= five_days_ago):
            news_obj = article_data(self, response)
            print(news_obj)
            PostNews.postnews(news_obj)
