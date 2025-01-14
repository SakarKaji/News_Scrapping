import scrapy
import re
from datetime import datetime, timedelta
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews
from news.article_object import article_data


class EverestHeadlineScrapper(scrapy.Spider):
    name = "EverestHeadline"
    # start_urls = ["https://www.everestheadlines.com/"]

    def __init__(self):
        self.articlelink_xpath = "//div/div[1]/div[1]/div[2]/li//h5/a/@href"
        self.description_xpath = '//div[contains(@class,"single-content")]/p'
        self.title_xpath = '//div/div[1]/div[1]/div[1]/div[1]/div/div/h1[2]/text()'
        self.image_xpath = '//div/div[1]/div[1]/div[1]/div[1]/div/div/div[6]/img/@src'
        self.date_xpath = '(//div[@class ="single-date"])[2]/span/text()'
        self.article_source = 'EverestHeadlines'
        self.categories = {
            Standard_Category.POLITICS: r"https://www.everestheadlines.com/category/politics",
            Standard_Category.OPINION: r"https://www.everestheadlines.com/category/oped",
            Standard_Category.SPORTS: r"https://www.everestheadlines.com/category/sports",
            Standard_Category.EDUCATION: r"https://www.everestheadlines.com/category/education",
            Standard_Category.TRAVEL: r"https://www.everestheadlines.com/category/tourism",
            Standard_Category.BUSINESS: r"https://www.everestheadlines.com/category/business",
            Standard_Category.INTERNATIONAL: r"https://www.everestheadlines.com/category/international",
            Standard_Category.OTHERS: r"https://www.everestheadlines.com/category/news",
        }

    def start_requests(self):
        for category in self.categories:
            try:
                yield scrapy.Request(url=self.categories[category], callback=self.parse, meta={'category': category})
            except Exception as e:
                print(f"Error:{e}")
                continue

    def parse(self, response):
        links = response.xpath(self.articlelink_xpath).getall()
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_article, meta={'category': response.meta['category']})

    def parse_article(self, response):
        date = response.xpath(self.date_xpath).get()
        self.formattedDate = Utils.everestHeadlines_conversion(date)
        five_days_ago = datetime.now() - timedelta(days=5)
        if self.formattedDate and (datetime.strptime(self.formattedDate, "%Y-%m-%d") >= five_days_ago):
            news_obj = article_data(self, response)
            news_obj["content_description"] = re.sub(
                r'(\xa0|<strong>|</strong>|<p[^>]*>|</p>|<source[^>]*>|</source>)', '',
                news_obj["content_description"]
            )
            # Remove extra spaces or newlines after cleaning
            news_obj["content_description"] = news_obj["content_description"].strip()
            print(news_obj)
            PostNews.postnews(news_obj)
