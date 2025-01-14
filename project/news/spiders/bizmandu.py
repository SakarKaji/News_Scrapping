import scrapy
from datetime import datetime, timedelta
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews


class bizamandu_scrapper(scrapy.Spider):
    name = "bizmandu"

    def __init__(self):
        self.articleslink_xpath = '//div[@class="news-img"]/a/@href'
        self.description_xpath = '//div[@class="news-text mb-0"]/p/text()'
        self.title_xpath = '//h1[@class="title-xxl detail_title"]/text()'
        self.image_xpath = '//div[@class="coverimage wp-block-image"]/img/@src'
        self.date_xpath = '//div[@class="author"]/div[@class="right-icon"]/span/text()'
        self.source = "ekantipur"
        self.categories = {
            Standard_Category.ECONOMY: r'https://bizmandu.com/content/category/market.html',
            Standard_Category.BUSINESS: r'https://bizmandu.com/content/category/corporate.html',
            Standard_Category.ECONOMY: r'https://bizmandu.com/content/category/banking.html',
            Standard_Category.LIFESTYLE: r'https://bizmandu.com/content/category/life-style.html',
            Standard_Category.OTHERS: r'https://bizmandu.com/content/category/special.html',
            Standard_Category.SCIENCE_AND_TECHNOLOGY: r'https://bizmandu.com/content/category/auto.html',
            Standard_Category.OTHERS: r'https://bizmandu.com/content/category/photo-news.html',
            Standard_Category.OTHERS: r'https://bizmandu.com/content/category/news.html',

        }

    def start_requests(self):
        print("---------Scraping bizmandu-----------")
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
        formattedDate = Utils.bizmandu_datetime(date)
        five_days_ago = datetime.now() - timedelta(days=5)
        if formattedDate and (datetime.strptime(formattedDate, "%Y-%m-%d") >= five_days_ago):
            url = response.url
            category = response.meta['category']
            title = response.xpath(self.title_xpath).get()
            descriptions = response.xpath(self.description_xpath).getall()
            desc = ''.join(descriptions)
            content = Utils.word_60(desc)
            img_src = response.xpath(self.image_xpath).get()
            unwanted_chars = ['\xa0', '\n', '\u202f', '\u200d', '\u200c']
            for char in unwanted_chars:
                content = content.replace(char, '')
            news = {
                'title': title.strip(),
                'content_description': content,
                'published_date': formattedDate,
                'url': url,
                'category': category,
                'is_recent': True,
                'source': 'bizmandu'
            }
            if img_src:
                news['image_url'] = img_src
            print(news)
            PostNews.postnews(news)
