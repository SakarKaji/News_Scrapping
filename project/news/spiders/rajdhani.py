import scrapy
from datetime import datetime, timedelta
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews


class rajdhanidaily_scrapper(scrapy.Spider):
    name = "rajdhanidaily"

    def __init__(self):
        self.articleslink_xpath = '//div[@class="elementor-post__card"]/a/@href'
        self.description_xpath = '//div[@class="elementor-widget-container"]/p/text()'
        self.title_xpath = '//h1[@class="elementor-heading-title elementor-size-default"]/text()'
        self.image_xpath = '//figure[@class="wp-caption"]/img/@src'
        self.date_xpath = '//span[@class="elementor-icon-list-text elementor-post-info__item elementor-post-info__item--type-date"]/text()'
        self.categories = {
            Standard_Category.SPORTS: r"https://rajdhanidaily.com/id/category/%e0%a4%96%e0%a5%87%e0%a4%b2/",
            Standard_Category.OPINION: r"https://rajdhanidaily.com/id/category/%e0%a4%ac%e0%a4%bf%e0%a4%9a%e0%a4%be%e0%a4%b0/",
            Standard_Category.INTERNATIONAL: r'https://rajdhanidaily.com/id/category/%e0%a4%85%e0%a4%a8%e0%a5%8d%e0%a4%a4%e0%a4%b0%e0%a4%be%e0%a4%b7%e0%a5%8d%e0%a4%9f%e0%a5%8d%e0%a4%b0%e0%a4%bf%e0%a4%af/',
            Standard_Category.OTHERS: r'https://rajdhanidaily.com/id/category/%e0%a4%b8%e0%a5%8c%e0%a4%9c%e0%a4%a8%e0%a5%8d%e0%a4%af/',
            Standard_Category.OTHERS: r'https://rajdhanidaily.com/id/category/%e0%a4%aa%e0%a5%8d%e0%a4%b0%e0%a4%b5%e0%a4%be%e0%a4%b8/',
            Standard_Category.ECONOMY: r'https://rajdhanidaily.com/id/category/%e0%a4%85%e0%a4%b0%e0%a5%8d%e0%a4%a5/',
            Standard_Category.SOCIETY: r'https://rajdhanidaily.com/id/category/%e0%a4%b8%e0%a4%ae%e0%a4%be%e0%a4%9c/',
            Standard_Category.POLITICS: r'https://rajdhanidaily.com/id/category/%e0%a4%b0%e0%a4%be%e0%a4%9c%e0%a4%a8%e0%a5%80%e0%a4%a4%e0%a4%bf/',
            Standard_Category.ART: r'https://rajdhanidaily.com/id/category/kala/'
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
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_article, meta={'category': response.meta['category']})

    def parse_article(self, response):
        date = response.xpath(self.date_xpath).get()
        formattedDate = Utils.rajdhani_conversion(date)
        five_days_ago = datetime.now() - timedelta(days=5)
        if formattedDate and (datetime.strptime(formattedDate, "%Y-%m-%d") >= five_days_ago):
            url = response.url
            category = response.meta['category']
            title = response.xpath(self.title_xpath).get()
            descriptions = response.xpath(self.description_xpath).getall()
            desc = ''.join(descriptions)
            content = Utils.word_60(desc)
            img_src = response.xpath(self.image_xpath).get()
            news = {
                'title': title.strip(),
                'content_description': content,
                'published_date': formattedDate,
                'image_url': img_src,
                'url': url,
                'category': category,
                'is_recent': True,
                'source': 'rajdhanidaily'
            }
            print(news)
            PostNews.postnews(news)
