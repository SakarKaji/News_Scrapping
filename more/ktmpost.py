import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime


class KathmanduPost(scrapy.Spider):
    name = "kathmandu_post"
    start_urls = ['https://kathmandupost.com']

    def initialize(self):
        self.title_xpath = '//h1[@style]/text()'
        self.date_xpath = '//div[@class="updated-time"]/text()'
        self.img_src_xpath = '//div[contains(@class,"row")]/div/img/@data-src'
        self.description_xpath = '//section/p/text()'

        self.categories_xpath = '//ul[@class="list-inline"][@style="display:inline-block;"]/li'
        self.articles_xpath = '//article[@class="article-image "]'
        self.article_link_xpath='.//a/@href'
        self.link_xpath = './/a'

        self.news = []
        self.categories = {}

    def parse(self, response):
        self.initialize()
        categories = response.xpath(self.categories_xpath)

        for category in categories:
            category_link = category.xpath('.//a/@href').get()
            category_text = category.xpath('.//a/text()').get()

            if category_text in self.categories:
                self.categories[category_text].append(category_link)
            else:
                self.categories[category_text] = [category_link]

        for category_text, category_links in self.categories.items():
            for category_link in category_links:
                try:
                    yield scrapy.Request(url=response.urljoin(category_link), 
                                        callback=self.find_article_links,
                                        meta={'category': category_text})
                except Exception as e:
                    print("Error: ", e)

    def find_article_links(self, response):
        category_text = response.meta['category']
        articles = response.xpath(self.articles_xpath)[:5]

        for article in articles:
            article_link = article.xpath(self.article_link_xpath).get()
            yield scrapy.Request(url = response.urljoin(article_link), 
                                 callback = self.parse_article,
                                 meta = {'category': category_text})

    def parse_article(self, response):
        category_text = response.meta['category']
        title = response.xpath(self.title_xpath).get().strip()

        article_date = response.xpath(self.date_xpath).get()
        published_date_str = article_date.split(':', 1)[-1].strip()
        try:
            date_object = datetime.strptime(published_date_str, '%B %d, %Y')
            formatted_date = date_object.strftime('%Y-%m-%d')
        except ValueError as e:
            print(f"Error parsing date: {e}")

        desc = response.xpath(self.description_xpath).getall()
        description = ''.join(desc)

        img_src = response.xpath(self.img_src_xpath).get()

        category_mapping = {
            'National': 'Others',
            'Valley': 'Others',
            'Money': 'Finance',
            'Culture & Lifestyle': 'Culture'
        }

        category_text = category_mapping.get(category_text, category_text)

        article_data = {
            'category_name': category_text,
            'title': title,
            'published_date': formatted_date,
            'content_description': description[:100],
            'img_url': img_src,
            'url': response.url,
        }

        self.news.append(article_data)

        # for news in self.news:
        #     print(news)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'LOG_ENABLED': False,
    'LOG_STDOUT': False,
})

process.crawl(KathmanduPost)
process.start()
