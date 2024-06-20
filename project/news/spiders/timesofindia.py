import scrapy
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews
import time
class timesofindia_scrapper(scrapy.Spider):
    name = "timesofindia"

    def __init__(self):
        self.articles_xpath = '//div[@class="col_l_2 col_m_3"]//figure/a/@href'
        self.description_xpath = '//div[@class="_s30J clearfix  "]/text()'
        self.title_xpath = '//h1[@class="HNMDR"]/span/text()'
        self.image_xpath = '//div[@class="wJnIp"]/img/@src'
        self.date_xpath = '//div[@class="published-date col-md-6"]/span/text()[1]'
        self.date_xpath_2 = '//div[@class="xf8Pm byline"]/span/text()'
        self.categories = {
            Standard_Category.SPORTS: r"https://timesofindia.indiatimes.com/sports",
            Standard_Category.OTHERS: r"https://timesofindia.indiatimes.com/india",
            Standard_Category.INTERNATIONAL: r'https://timesofindia.indiatimes.com/world',
            Standard_Category.ENTERTAINMENT: r'https://timesofindia.indiatimes.com/etimes',
            Standard_Category.SCIENCE_AND_TECHNOLOGY: r'https://timesofindia.indiatimes.com/technology',
            Standard_Category.SCIENCE_AND_TECHNOLOGY: r'https://timesofindia.indiatimes.com/auto',
            Standard_Category.BUSINESS: r'https://timesofindia.indiatimes.com/business',
            Standard_Category.EDUCATION: r'https://timesofindia.indiatimes.com/education',
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
        time.sleep(3)
        url = response.url
        category = response.meta['category']
        title = response.xpath(self.title_xpath).extract_first()
        img_src = response.xpath(self.image_xpath).extract_first()
        descriptions = response.xpath(self.description_xpath).getall()
        desc = ''.join(descriptions)
        content = Utils.word_60(desc)
        date = response.xpath(self.date_xpath).get()
        if date == None:
            date = response.xpath(self.date_xpath_2).get()
        formattedDate = Utils.time_of_india_date_convertor1(date)
        news = {
            'title':title.strip(),
            'content_description':content,
            'published_date':formattedDate,
            'image_url':img_src,
            'url':url,
            'category_name':category,
            'is_recent':True,
            'source_name':'timesofindia'
            }
        PostNews.postnews(news)
