
import scrapy
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews
import time

class reportersnepal_scrapper(scrapy.Spider):
    name = "reportersnepal"

    def __init__(self):
        self.articleslink_xpath_main = '//div[@class="wrap mb-4 text-center"]/a/@href'
        self.articleslink_xpath= '//a[@class="post-list d-flex"]/@href'
        self.description_xpath = '//article[@class="post-entry"]/p/text()'
        self.title_xpath = '//h1[@class="single-heading text-center"]/text()'
        self.image_xpath = '//figure[@class="p-1 b-1 rounded mx-auto d-block"]/img/@src'
        self.date_xpath = '//div[@class="post-date"]/text()[2]'
        self.categories = {
            Standard_Category.OTHERS: r'https://reportersnepal.com/category/%e0%a4%a7%e0%a4%b0%e0%a5%8d%e0%a4%ae-%e0%a4%b8%e0%a4%82%e0%a4%b8%e0%a5%8d%e0%a4%95%e0%a5%83%e0%a4%a4%e0%a4%bf/',
            Standard_Category.OTHERS: r'https://reportersnepal.com/category/rochak/',
            Standard_Category.OTHERS: r'https://www.lokaantar.com/category/national',
            Standard_Category.SOCIETY: r'https://www.lokaantar.com/category/society',
            Standard_Category.SCIENCE_AND_TECHNOLOGY: r'https://www.reportersnepal.com/category/technology',
            Standard_Category.OTHERS: r'https://reportersnepal.com/category/others/',
            Standard_Category.ENTERTAINMENT: r'https://www.reportersnepal.com/category/entertainment',
            Standard_Category.BUSINESS: r'https://www.reportersnepal.com/category/business',
            Standard_Category.INTERNATIONAL: r'https://www.reportersnepal.com/category/world',
            Standard_Category.OPINION: r'https://www.reportersnepal.com/category/thoughts',
            Standard_Category.SPORTS: r'https://www.reportersnepal.com/category/sports',
            Standard_Category.POLITICS: r'https://www.reportersnepal.com/reportersnepal/politics',
            Standard_Category.HEALTH: r'https://reportersnepal.com/category/health/',
            Standard_Category.OTHERS: r'https://reportersnepal.com/category/featured/'
        }
        

    def start_requests(self):
        for category in self.categories:
            try:
                yield scrapy.Request(url=self.categories[category], callback=self.parse, meta={'category': category})
            except Exception as e:
                print(f"Error:{e}")
                continue

    def parse(self, response):
        link1= response.xpath(self.articleslink_xpath_main).getall()
        link2 = response.xpath(self.articleslink_xpath).getall()
        links = link1 + link2
        for link in links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_article, meta={'category': response.meta['category']})


    def parse_article(self, response):
        url = response.url
        category = response.meta['category']
        title = response.xpath(self.title_xpath).get()
        descriptions = response.xpath(self.description_xpath).getall()
        desc = ''.join(descriptions)
        content = Utils.word_60(desc)
        img_src = response.xpath(self.image_xpath).get()
        date = response.xpath(self.date_xpath).get()
        formattedDate = Utils.reportersnepal_conversion(date)

        news = {
            'title':title.strip(),
            'content_description':content,
            'published_date':formattedDate,
            'image_url':img_src,
            'url':url,
            'category_name':category,
            'is_recent':True,
            'source_name':'reportersnepal'
            }
        PostNews.postnews(news)