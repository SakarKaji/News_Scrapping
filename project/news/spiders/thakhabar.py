import scrapy
from datetime import datetime, timedelta
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews
import time


class Thakhabar_scrapper(scrapy.Spider):
    name = "thakhabar"

    def __init__(self):
        self.articleslink_xpath = '//div[@class="mb-15 "]/h3/a/@href'
        self.description_xpath = '//div[@class="post-body"]//p/text()'
        self.title_xpath = '//div[@class="heading-title-50 mb-15"]/h1/a/text()'
        self.image_xpath = '//div[@class="detail-title-img mb-30"]//a/img/@src'
        self.date_xpath = '//span[@class="post-date-grey"]/text()'
        self.categories = {
            Standard_Category.SPORTS: r"https://thahakhabar.com/category/sports/",
            Standard_Category.OPINION: r"https://thahakhabar.com/category/opinion/",
            Standard_Category.INTERNATIONAL: r'https://thahakhabar.com/category/international/',
            Standard_Category.OTHERS: r'https://thahakhabar.com/category/interview/',
            Standard_Category.OTHERS: r'https://thahakhabar.com/category/feature/',
            Standard_Category.ECONOMY: r'https://thahakhabar.com/category/economy/',
            Standard_Category.SOCIETY: r'https://thahakhabar.com/category/society/',
            Standard_Category.POLITICS: r'https://thahakhabar.com/category/politics/',
            Standard_Category.ART: r'https://thahakhabar.com/category/arts/'
        }

    def start_requests(self):
        for category in self.categories:
            try:
                yield scrapy.Request(url=self.categories[category], callback=self.parse, meta={'category': category})
            except Exception as e:
                print(f"Error:{e}")
                continue

    def parse(self, response):
        time.sleep(2)
        links = response.xpath(self.articleslink_xpath).getall()
        for link in links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_article, meta={'category': response.meta['category']})

    def parse_article(self, response):
        time.sleep(5)
        date = response.xpath(self.date_xpath).get()
        formattedDate = Utils.thahakhabar_conversion(date)
        five_days_ago = datetime.now() - timedelta(days=5)
        if formattedDate and (datetime.strptime(formattedDate, "%Y-%m-%d") >= five_days_ago):
            url = response.url
            category = response.meta['category']
            title = response.xpath(self.title_xpath).get()
            descriptions = response.xpath(self.description_xpath).getall()
            desc = ''.join(descriptions)
            content = Utils.word_60(desc)
            img_src = response.xpath(self.image_xpath).get()

            unwanted_chars = ['\xa0', '\n']
            for char in unwanted_chars:
                content = content.replace(char, '')
            news = {
                'title': title.strip(),
                'content_description': content,
                'published_date': formattedDate,
                'image_url': img_src,
                'url': url,
                'category': category,
                'is_recent': True,
                'source': 'thahakhabar'
            }
            print(news)
            PostNews.postnews(news)


if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'LOG_ENABLED': False,
        'LOG_STDOUT': False,
    })
