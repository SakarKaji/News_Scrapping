import scrapy
from Utils import Utils
from Utils import PostNews
from Utils.Constants import Standard_Category
from news.article_object import article_data
from news.check_scrapy_links import collect_none_values
from Utils.Email import error_report_email


class Ratopati_scrapper(scrapy.Spider):
    name = "Ratopati Nepali"

    def __init__(self):
        self.articlelink_xpath = 'https://www.ratopati.com/'
        self.navPath = '//nav/div/div/div[1]/ul/li'
        self.articles_path = '//div[contains(@class,"columnnews mbl-col col3")]/a/@href'
        self.articles_path_sports = '//div[contains(@class,"thumbnail-news")]/a/@href'
        self.articles_path_entertainment = '//div[@class="thumbnail-news col4"]/a/@href'
        self.title_xpath = "//h2[contains(@class,'heading')]/text()"
        self.date_xpath = "//div[@class='newsInfo']/div[@class='post-hour']/span/text()"
        self.description_xpath = "//div[@class='the-content']/p/text()"
        self.image_xpath = "//figure[@class='featured-image']/img/@src"
        self.article_source = 'ratopati'

    def start_requests(self):
        yield scrapy.Request(url=self.articlelink_xpath, callback=self.parse)

    def parse(self, response):
        for link in response.xpath(self.navPath):
            category = link.xpath(".//a/text()").get()
            category_link = link.xpath(".//a/@href").get()
            if category and category_link != None:
                yield scrapy.Request(url=category_link,  callback=self.scrape_each_category, meta={"category": category})

    def scrape_each_category(self, response):
        if ((response.meta['category'].strip()) == "खेलकुद"):
            links = response.xpath(self.articles_path_sports).getall()

        if ((response.meta['category'].strip()) == "मनोरञ्जन"):
            links = response.xpath(self.articles_path_entertainment).getall()

        if ((response.meta['category'].strip()) != "मनोरञ्जन" and (response.meta['category'].strip()) != "खेलकुद"):
            links = response.xpath(self.articles_path).getall()

        count = 5
        if (count > 0):
            count = count - 1
            for each_link in links:
                yield scrapy.Request(url=each_link, callback=self.scrape_each_article, meta={"link": each_link, "category": response.meta['category']})

    def scrape_each_article(self, response):
        date = response.xpath(self.date_xpath).get()
        self.formattedDate = Utils.ratopati_date_conversion(date)

        category_name = 'Others' if getattr(
            Standard_Category, response.meta['category'], None) is None else response.meta['category']
        response.meta['category'] = category_name

        news_obj = article_data(self, response)
        PostNews.postnews(news_obj)
