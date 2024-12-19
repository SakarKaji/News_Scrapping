import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.reactor import install_reactor
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews
import logging


class AnnapurnaScraper(scrapy.Spider):
    name = "Annapurna"

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
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
        self.articlelink_xpath = '//div[@class="category__news"]/div[@class="custom-container"]/div[@class="category__news-grid"]'
        self.article_xpath = './/div[@class="grid__card"]'
        self.image_xpath = './/div[@class="card__img"]/a/img/@src'
        self.title_xpath = './/div[@class="card__details"]/h3/a/text()'
        self.article_link_xpath = './/div[@class="card__details"]/h3/a/@href'
        self.main_section_xpath = '//div[@class="ap__news-content"]'
        self.description_xpath = './/div[@class="news__details"]/p/text()'
        self.date_xpath = './/p[@class="date"]/span/text()'
        self.categories = {
            Standard_Category.POLITICS: r'https://www.annapurnapost.com/category/politics/',
            Standard_Category.SOCIETY: r'https://www.annapurnapost.com/category/social/',
            Standard_Category.ECONOMY: r'https://www.annapurnapost.com/category/economy/',
            Standard_Category.OPINION: r'https://www.annapurnapost.com/category/opinion/',
            Standard_Category.SPORTS: r'https://www.annapurnapost.com/category/sports/',
            Standard_Category.ENTERTAINMENT: r'https://www.annapurnapost.com/category/entertainment/',
            Standard_Category.SCIENCE_AND_TECHNOLOGY: r'https://www.annapurnapost.com/category/science/',
            # Standard_Category.SCIENCE_AND_TECHNOLOGY: r'https://www.annapurnapost.com/category/tech/',
            Standard_Category.HEALTH: r'https://www.annapurnapost.com/category/health/',
            Standard_Category.LIFESTYLE: r'https://www.annapurnapost.com/category/lifestyle/',
            Standard_Category.EDUCATION: r'https://www.annapurnapost.com/category/education/',
            Standard_Category.TRAVEL: r'https://www.annapurnapost.com/category/travel/',
            Standard_Category.FASHION: r'https://www.annapurnapost.com/category/fashion/',
            Standard_Category.BUSINESS: r'https://www.annapurnapost.com/category/business/',
            Standard_Category.INTERNATIONAL: r'https://www.annapurnapost.com/category/international/',
            Standard_Category.FINANCE: r'https://www.annapurnapost.com/category/finance/',
            Standard_Category.ART: r'https://www.annapurnapost.com/category/art/',
            Standard_Category.WEATHER: r'https://www.annapurnapost.com/category/weather/',
            Standard_Category.OTHERS: r'https://www.annapurnapost.com/category/others/'
        }
        print('Scraping AnnapurnaPost')

    def start_requests(self):
        for category in self.categories:
            link = self.categories[category]
            print(link)
            try:
                yield scrapy.Request(url=self.categories[category], callback=self.parse, meta={'category': category})

            except Exception as e:
                print(f"Error:{e}")
                continue

    def parse(self, response):
        articles = response.xpath(self.articlelink_xpath)
        for article in articles.xpath(self.article_xpath):
            # image_link = article.xpath(self.image_xpath).get().strip()
            image_link = article.xpath(self.image_xpath)
            title = article.xpath(self.title_xpath).get().strip()
            get_link = article.xpath(self.article_link_xpath).get()
            link = f"https://www.annapurnapost.com{get_link}"
            yield scrapy.Request(url=link, callback=self.parse_article, meta={'title': title, 'link': link, 'img_link': image_link, 'category': response.meta['category']})

    def parse_article(self, response):
        title = response.meta['title']
        link = response.meta['link']
        img_src = response.meta['img_link']
        category = response.meta['category']
        main_section = response.xpath(self.main_section_xpath)
        description_elements = main_section.xpath(self.description_xpath)
        description = ""
        for item in description_elements:
            description = description + item.get().strip() + "\n"

        description = description.strip()
        content = Utils.word_60(description)
        date = main_section.xpath(self.date_xpath).get()
        published_date = Utils.annapurnapost_datetime(date)

        news = {
            'title': title.replace('\xa0', ''),
            'content_description': content,
            'published_date': published_date,
            'image_url': img_src,
            'url': link,
            'category': category,
            'is_recent': True,
            'source': 'annapurnapost'
        }
        print(news)
        PostNews.postnews(news)
