import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.reactor import install_reactor
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews


class EverestHeadlineScrapper(scrapy.Spider):
    name = "EverestHeadline"

    def __init__(self):
        self.articles_xpath = "//div/div[1]/div[1]/div[2]/li//h5/a/@href"
        self.description_xpath = '//div[contains(@class,"single-content")]/p'
        self.title_xpath = '//div/div[1]/div[1]/div[1]/div[1]/div/div/h1[2]/text()'
        self.image_xpath = "//div/div[1]/div[1]/div[1]/div[1]/div/div/div[6]/img/@src"
        self.date_xpath = '(//div[@class ="single-date"])[2]/span/text()'
        self.categories = {
            Standard_Category.POLITICS: r"https://www.everestheadlines.com/category/politics",
            Standard_Category.OPINION: r"https://www.everestheadlines.com/category/oped",
            Standard_Category.SPORTS: r"https://www.everestheadlines.com/category/sports",
            Standard_Category.EDUCATION: r"https://www.everestheadlines.com/category/education",
            Standard_Category.TRAVEL: r"https://www.everestheadlines.com/category/tourism",
            Standard_Category.BUSINESS: r"https://www.everestheadlines.com/category/business",
            Standard_Category.INTERNATIONAL: r"https://www.everestheadlines.com/category/international",
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
        count = 5
        if(count>0):
            for link in links:
                count -= 1
                yield scrapy.Request(url=link, callback=self.parse_article, meta={'category': response.meta['category']})


    def parse_article(self, response):
        url = response.url
        category = response.meta['category']
        title = response.xpath(self.title_xpath).get()        
        img_src = response.xpath(self.image_xpath).get()
        descriptions = response.xpath(self.description_xpath).getall()
        desc = ''.join(descriptions)
        content = Utils.word_60(desc)
        date = response.xpath(self.date_xpath).get()
        formattedDate = Utils.everestHeadlines_conversion(date)

        news = {
            'title':title,
            'content_description':content,
            'published_date':formattedDate,
            'image_url':img_src,
            'url':url,
            'category_name':category,
            'is_recent':True,
            'source_name':'EverestHeadlines'
            }
        PostNews.postnews(news)
        print(f"---------------category_name: {category},---------------------")