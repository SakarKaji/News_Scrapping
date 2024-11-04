import scrapy
from datetime import datetime, timedelta
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews


class arthasarokar_scrapper(scrapy.Spider):
    name = "arthasarokar"

    def __init__(self):
        self.articleslink_xpath = '//div[@class="site-content"]//a/@href'
        self.description_xpath = '//div[@class="entry-content"]/p/text()'
        self.title_xpath = '//h1[@class="entry-title"]/text()'
        self.image_xpath = '//div[@class="post-thumbnail"]/img/@src'
        self.date_xpath = '//p[@class="pub-date"]/text()'
        self.categories = {
            Standard_Category.INTERNATIONAL: r'https://arthasarokar.com/category/international-economy',
            Standard_Category.ECONOMY: r'https://arthasarokar.com/category/banking',
            Standard_Category.TRAVEL: r'https://arthasarokar.com/category/tourism',
            Standard_Category.ECONOMY: r'https://arthasarokar.com/category/market-affairs',
            Standard_Category.BUSINESS: r'https://arthasarokar.com/category/corporate',
            Standard_Category.OTHERS: r'https://arthasarokar.com/category/bhansa',
            Standard_Category.OTHERS: r'https://arthasarokar.com',
            Standard_Category.ECONOMY: r'https://arthasarokar.com/category/insurance'
        }

    def start_requests(self):
        print("---------Scraping Arthasarokar-----------")
        for category in self.categories:
            try:
                yield scrapy.Request(url=self.categories[category], callback=self.parse, meta={'category': category})
            except Exception as e:
                print(f"Error:{e}")
                continue

    def parse(self, response):
        links = response.xpath(self.articleslink_xpath).getall()
        for link in links:
            if link.endswith(".html"):
                yield scrapy.Request(url=response.urljoin(link), callback=self.parse_article, meta={'category': response.meta['category']})

    def parse_article(self, response):
        date = response.xpath(self.date_xpath).get()
        formattedDate = Utils.ArthaSarokar_conversion(date)
        five_days_ago = datetime.now() - timedelta(days=5)
        if formattedDate and (datetime.strptime(formattedDate, "%Y-%m-%d") >= five_days_ago):
            url = response.url
            category = response.meta['category']
            title = response.xpath(self.title_xpath).get()
            descriptions = response.xpath(self.description_xpath).getall()
            desc = ''.join(descriptions)
            content = Utils.word_60(desc)
            img_src = response.xpath(self.image_xpath).get()

            unwanted_chars = ['\xa0', '\n', '\r']
            for char in unwanted_chars:
                content = content.replace(char, '')
            news = {
                'title': title.strip(),
                'content_description': content.strip(),
                'published_date': formattedDate,
                'image_url': img_src,
                'url': url,
                'category': category,
                'is_recent': True,
                'source': 'arthasarokar'
            }
            print(news)
            PostNews.postnews(news)
