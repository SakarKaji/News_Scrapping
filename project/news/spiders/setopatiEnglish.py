import scrapy
from datetime import datetime, timedelta
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews


class SetopatiEnglish_Scrapper(scrapy.Spider):
    name = "setopatienglish"

    def __init__(self):
        self.articles_xpath = '//*[@id="content"]/div/section/div/div/a/@href'
        self.description_xpath = "//*[@id='content']/div/div/aside/div[1]/div/div[1]/p/text()"
        self.title_xpath = "//*[@id='content']/div/section/div[1]/span/text()"
        self.image_xpath = '//div[@class="featured-images col-md-12"]/figure/img/@src'
        self.date_xpath = '//div[@class="published-date col-md-6"]/span/text()[1]'
        self.categories = {
            Standard_Category.SPORTS: r"https://en.setopati.com/sports",
            Standard_Category.OPINION: r"https://en.setopati.com/view",
            Standard_Category.SOCIETY: r'https://en.setopati.com/social',
            Standard_Category.INTERNATIONAL: r'https://en.setopati.com/International',
            # Standard_Category.ART: r'https://www.setopati.com/category/art',
            Standard_Category.ENTERTAINMENT: r'https://en.setopati.com/entertainment',
            # Standard_Category.ART: r'https://www.setopati.com/art/art-activity',
            Standard_Category.OTHERS: r'https://www.setopati.com/nepali-brand',
            Standard_Category.BUSINESS: r'https://en.setopati.com/market',
            Standard_Category.OTHERS: r'https://en.setopati.com/blog',
        }

    def start_requests(self):
        for category in self.categories:
            try:
                yield scrapy.Request(url=self.categories[category], callback=self.parse, meta={'category': category})
            except Exception as e:
                print(f"Error:{e}")
                continue

    def parse(self, response):
        links = response.xpath(self.articles_xpath).getall()
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_article, meta={'category': response.meta['category']})

    def parse_article(self, response):
        date = response.xpath(self.date_xpath).get()
        formattedDate = Utils.setopatienglish_datetime(date)
        five_days_ago = datetime.now() - timedelta(days=5)
        if formattedDate and (datetime.strptime(formattedDate, "%Y-%m-%d") >= five_days_ago):
            url = response.url
            category = response.meta['category']
            title = response.xpath(self.title_xpath).get()
            img_src = response.xpath(self.image_xpath).get()
            descriptions = response.xpath(self.description_xpath).getall()
            desc = ''.join(descriptions)
            content = Utils.word_60(desc)

            unwanted_chars = ['\xa0', '\n', '\r']
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
                'source': 'setopatienglish'
            }
            print(news)
            PostNews.postnews(news)
