
import scrapy
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews


class News24Scrapper(scrapy.Spider):
    name = "news24"

    def __init__(self):
        self.articles_xpath = '//div[contains(@class,"item-details")]/h3/a/@href'
        self.description_xpath = '//div[@class="td-post-content td-pb-padding-side"]/p/text()'
        self.title_xpath = '//header/h1/text()'
        self.image_xpath = '//div[contains(@class,"td-post-featured-image")]/a/img/@src'
        self.date_xpath = '//header/div/span[@class="td-post-date"]/time/text()'
        self.categories = {
            Standard_Category.SPORTS: r"https://news24nepal.tv/category/sports/",
            Standard_Category.OPINION: r"https://news24nepal.tv/category/ideas/",
            Standard_Category.INTERNATIONAL: r'https://news24nepal.tv/category/world/',
            Standard_Category.ENTERTAINMENT: r'https://news24nepal.tv/category/entertainment/',
            Standard_Category.OTHERS: r'https://news24nepal.tv/category/videos/',
            Standard_Category.BUSINESS: r'https://news24nepal.tv/category/business/',
            Standard_Category.OTHERS: r'https://news24nepal.tv/category/news/',
            Standard_Category.POLITICS: r'https://news24nepal.tv/category/news/poltical/'
        }
        

    def start_requests(self):
        for category in self.categories:
            try:
                yield scrapy.Request(url=self.categories[category], callback=self.parse, meta={'category': category})
            except Exception as e:
                print(f"Error:{e}")
                continue

    def parse(self, response):
        links= response.xpath(self.articles_xpath).getall()
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
        formattedDate = Utils.news24_conversion(date)

        news = {
            'title':title.strip(),
            'content_description':content,
            'published_date':formattedDate,
            'image_url':img_src,
            'url':url,
            'category_name':category,
            'is_recent':True,
            'source_name':'News24'
            }
        PostNews.postnews(news)
