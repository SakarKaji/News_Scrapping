import scrapy
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews


class Onlinemajdur_scrapper(scrapy.Spider):
    name = "onlinemajdur"

    def __init__(self):
        self.articleslink_xpath = '//div[contains(@class,"content")]/h3/a/@href'
        self.description_xpath = '//div[@class="content single-news-text"]/p/text()'
        self.title_xpath = '//div[@class="single-news-contents"]/h1/text()'
        self.image_xpath = '//div[@class="single-news-contents"]/figure/img/@src'
        self.date_xpath = '//div[@class="single-news-contents"]/ul/li[1]/span/text()[2]'
        self.categories = {
            Standard_Category.HEALTH: r"https://onlinemajdoor.com/?cat=13",
            Standard_Category.OPINION: r"https://onlinemajdoor.com/?cat=3",
            Standard_Category.OPINION: r"https://onlinemajdoor.com/?cat=17",
            Standard_Category.INTERNATIONAL: r'https://onlinemajdoor.com/?cat=5',
            Standard_Category.SPORTS: r'https://onlinemajdoor.com/?cat=11',
            Standard_Category.OTHERS: r'https://onlinemajdoor.com/?cat=15',
            Standard_Category.OTHERS: r'https://onlinemajdoor.com/?cat=14',
            Standard_Category.ART: r'https://onlinemajdoor.com/?cat=2',
            Standard_Category.POLITICS: r'https://onlinemajdoor.com/?cat=8',
            Standard_Category.EDUCATION: r'https://onlinemajdoor.com/?cat=20'
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
            yield scrapy.Request(url=link, callback=self.parse_article, meta={'category': response.meta['category']})

    def parse_article(self, response):
        url = response.url
        category = response.meta['category']
        title = response.xpath(self.title_xpath).get()
        descriptions = response.xpath(self.description_xpath).getall()
        desc = ''.join(descriptions)
        content = Utils.word_60(desc)
        img_src = response.xpath(self.image_xpath).get()
        date = response.xpath(self.date_xpath).get()
        formattedDate = Utils.onlinemajdoor_date_conversion(date)

        news = {
            'title': title.strip(),
            'content_description': content,
            'published_date': formattedDate,
            'image_url': img_src,
            'url': url,
            'category': category,
            'is_recent': True,
            'source': 'onlinemajdoor'
        }
        PostNews.postnews(news)
