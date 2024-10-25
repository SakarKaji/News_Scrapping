import scrapy
import time
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews


class nayapage_scrapper(scrapy.Spider):
    name = "nayapage"

    def __init__(self):
        self.articleslink_xpath = '//div[@class="uk-grid uk-child-width-1-4@m uk-grid-stack"]//div/a/@href'
        self.description_xpath = '/article[@class="post-entry"]//p/text()'
        self.title_xpath = '/article[@class="post-entry"]//h1/text()'
        self.image_xpath = '//figure/img[@class="uk-width-1-1 wp-post-image"]/@src'
        self.date_xpath = '//div[@class="uk-flex uk-flex-middle uk-width-1@m uk-first-column"]//div[@class="uk-margin-small-left"]/text()'
        self.categories = {
            Standard_Category.OTHERS: r'https://nayapage.com/category/30',
            Standard_Category.ENTERTAINMENT: r'https://nayapage.com/category/20',
        }

    def start_requests(self):
        for category in self.categories:
            try:
                yield scrapy.Request(url=self.categories[category], callback=self.parse, meta={'category': category})
            except Exception as e:
                print(f"Error:{e}")
                continue

    def parse(self, response):
        links = response.xpath(self.articleslink_xpath).getall()
        for link in links:
            if link.startswith('https://nayapage.com/'):
                print(link)
                yield scrapy.Request(url=link, callback=self.parse_article, meta={'category': response.meta['category']})

    def parse_article(self, response):
        time.sleep(2)
        url = response.url
        category = response.meta['category']
        title = response.xpath(self.title_xpath).get()
        descriptions = response.xpath(self.description_xpath).getall()
        desc = ''.join(descriptions)
        content = Utils.word_60(desc)
        img_src = response.xpath(self.image_xpath).get()
        date = response.xpath(self.date_xpath).get().strip()
        formattedDate = Utils.nayapage_datetime(date)

        news = {
            'title': title.strip(),
            'content_description': content,
            'published_date': formattedDate,
            'image_url': img_src,
            'url': url,
            'category_name': category,
            'is_recent': True,
            'source_name': 'nayapage'
        }
        print(news)
        PostNews.postnews(news)
