import scrapy
from Utils import PostNews
from news.article_object import article_data


class bbcNepali_scrapper(scrapy.Spider):
    name = "bbcNepali"

    def __init__(self):
        self.articlelink_xpath = 'https://www.bbc.com/nepali'
        self.articles_xpath = '//div/div/section[1]/div/ul//h3[@class="bbc-1kr00f0 e47bds20"]/a/@href'
        self.description_xpath = '//*[@id="main-wrapper"]/div/div/div/div[1]/main/div/p/text()'
        self.title_xpath = '//*[@id="content"]/text()'
        self.image_xpath = '//div/div/div/div[1]/main/figure[1]/div/picture/img/@src'
        self.date_xpath = '//div/div/div/div[1]/main/div[2]/time/@datetime'
        self.article_source = 'bbcnepali'

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls, callback=self.parse)

    def parse(self, response):
        for link in response.xpath(self.articles_xpath).getall():
            yield scrapy.Request(url=link, callback=self.parse_article)

    def parse_article(self, response):
        self.formattedDate = response.xpath(self.date_xpath).get()
        news_obj = article_data(self, response)
        PostNews.postnews(news_obj)
