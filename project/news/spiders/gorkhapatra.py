import scrapy
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews
from news.article_object import article_data


class GorkhaPatraOnlineScrapper(scrapy.Spider):
    name = "Gorkhapatra"

    def __init__(self):
        self.articlelink_xpath = '//div[contains(@class,"item-content")]/h2/a/@href'
        self.description_xpath = '//div[@class="blog-details"]/p/text()'
        self.title_xpath = '//div[@class="col-lg-12"]/h1/text()'
        self.image_xpath = "//div[@class='blog-banner']/img/@src"
        self.date_xpath = '//*[@id="main"]/section/div/div[1]/div[1]/div[2]/div[2]/div[1]/div/div[2]/span/text()[2]'
        self.article_source = 'gorkhapatra'
        self.categories = {
            Standard_Category.POLITICS: r'https://gorkhapatraonline.com/categories/politics',
            Standard_Category.BUSINESS: r' https://gorkhapatraonline.com/categories/corporate',
            Standard_Category.ECONOMY: r'https://gorkhapatraonline.com/categories/economy',
            Standard_Category.ECONOMY: r'https://gorkhapatraonline.com/categories/bank',
            Standard_Category.ECONOMY: r'https://gorkhapatraonline.com/categories/share',
            Standard_Category.OPINION: r'https://gorkhapatraonline.com/categories/thoughts',
            Standard_Category.SPORTS: r'https://gorkhapatraonline.com/categories/sports',
            Standard_Category.ENTERTAINMENT: r'https://gorkhapatraonline.com/categories/entertainment',
            Standard_Category.SCIENCE_AND_TECHNOLOGY: r'https://gorkhapatraonline.com/categories/technology',
            Standard_Category.HEALTH: r'https://gorkhapatraonline.com/categories/health',
            Standard_Category.EDUCATION: r'https://gorkhapatraonline.com/categories/education',
            Standard_Category.INTERNATIONAL: r'https://gorkhapatraonline.com/categories/international',
            Standard_Category.ART: r'https://gorkhapatraonline.com/categories/culture-and-arts',
            Standard_Category.TRAVEL: r'https://gorkhapatraonline.com/categories/tourism',
        }

    def start_requests(self):
        for category in self.categories:
            try:
                yield scrapy.Request(url=self.categories[category], callback=self.parse, meta={'category': category})
            except Exception as e:
                print(f"Error:{e}")
                continue

    def parse(self, response):
        links = response.xpath(self.articlelink_xpath).getall()
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_article, meta={'category': response.meta['category']})

    def parse_article(self, response):
        date = response.xpath(self.date_xpath).get()
        self.formattedDate = Utils.gorkhapatraonline_datetime_parser(date)
        
        news_obj = article_data(self, response)
        PostNews.postnews(news_obj)
