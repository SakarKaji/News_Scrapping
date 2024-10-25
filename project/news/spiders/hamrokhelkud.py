
import scrapy
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews
import time


class hamrokhelkud_scrapper(scrapy.Spider):
    name = "hamrokhelkud"

    def __init__(self):
        self.articleslink_xpath = '//div[@class="left-list-wrapper"]/a/@href'
        self.description_xpath = '//div[@class="content-wrapper"]/p/text()'
        self.title_xpath = '//div[@class="second-row-content"]/h3/text()'
        self.image_xpath = '//div[@class="banner-wrapper"]/img/@data-src'
        self.date_xpath = '//div[@class="me-3 pe-3 inner-wrapper published-date-wrapper"]/p/text()'
        self.categories = {
            Standard_Category.INTERNATIONAL: r'https://www.hamrokhelkud.com/category/international',
            Standard_Category.SPORTS: r'https://www.hamrokhelkud.com/category/football',
            Standard_Category.SPORTS: r'https://www.hamrokhelkud.com/category/cricket',
            Standard_Category.SPORTS: r'https://www.hamrokhelkud.com/category/volleyball'
        }

    def start_requests(self):
        print("---------Scraping hamrokhelkud -----------")
        for category in self.categories:
            try:
                yield scrapy.Request(url=self.categories[category], callback=self.parse, meta={'category': category})
            except Exception as e:
                print(f"Error:{e}")
                continue

    def parse(self, response):
        links = response.xpath(self.articleslink_xpath).getall()
        for link in links:
            try:
                yield scrapy.Request(url=link, callback=self.parse_article, meta={'category': response.meta['category']})
            except Exception as e:
                print(f"Error in {link}")

    def parse_article(self, response):
        url = response.url
        category = response.meta['category']
        print(category)
        title = response.xpath(self.title_xpath).extract_first()
        descriptions = response.xpath(self.description_xpath).getall()
        desc = ''.join(descriptions)
        content = Utils.word_60(desc)
        img_src = response.xpath(self.image_xpath).get()
        date = response.xpath(self.date_xpath).get()
        formattedDate = Utils.hamrokhelkud_conversion(date)

        news = {
            'title': title.strip(),
            'content_description': content,
            'published_date': formattedDate,
            'image_url': img_src,
            'url': url,
            'category_name': category,
            'is_recent': True,
            'source_name': 'hamrokhelkud'
        }
        PostNews.postnews(news)
