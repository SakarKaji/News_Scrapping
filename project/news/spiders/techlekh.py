import scrapy
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews
from news.article_object import article_data


class techlekh_scrapper(scrapy.Spider):
    name = "techlekh"

    def __init__(self):
        self.articleslink_xpath = '//h2[@class="entry-title"]/a/@href'
        self.description_xpath = '//div[@class="entry-content wrap clearfix"]/p/text()'.replace(
            '\xa0', '')
        self.title_xpath = '//h1[@class="entry-title"]/text()'
        self.image_xpath = '(//figure[contains(@class,"wp-caption")]//img/@data-lazy-src)[1]'
        self.date_xpath = '//span[@class="date"]/text()[2]'
        self.article_source = 'techlekh'
        self.categories = {
            Standard_Category.SCIENCE_AND_TECHNOLOGY: r'https://techlekh.com/category/news/',
            Standard_Category.OTHERS: r'https://techlekh.com/category/events/',
            Standard_Category.OTHERS: r'https://techlekh.com/category/reviews/',
            Standard_Category.OTHERS: r'https://techlekh.com/category/deals/',
            Standard_Category.SCIENCE_AND_TECHNOLOGY: r'https://techlekh.com/category/auto/',
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
        self.formattedDate = Utils.techlekh_dateconverter(date)
        news_obj = article_data(self, response)
        PostNews.postnews(news_obj)
