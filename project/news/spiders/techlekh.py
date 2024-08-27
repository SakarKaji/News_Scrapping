import scrapy
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews
import logging


class techlekh_scrapper(scrapy.Spider):
    name = "techlekh"

    def __init__(self):
        self.articleslink_xpath = '//h2[@class="entry-title"]/a/@href'
        self.description_xpath = '//div[@class="entry-content wrap clearfix"]/p/text()'
        self.title_xpath = '//h1[@class="entry-title"]/text()'
        self.image_xpath = '//figure[@class="wp-caption aligncenter"]/img/@src'
        self.date_xpath = '//span[@class="date"]/text()[2]'
        self.categories = {
            Standard_Category.SCIENCE_AND_TECHNOLOGY: r'https://techlekh.com/category/news/',
            
            Standard_Category.OTHERS: r'https://techlekh.com/category/events/',

            Standard_Category.OTHERS: r'https://techlekh.com/category/reviews/',
            Standard_Category.OTHERS: r'https://techlekh.com/category/deals/',
            Standard_Category.SCIENCE_AND_TECHNOLOGY: r'https://techlekh.com/category/auto/',

       

            
        }
        

    def start_requests(self):
        print("---------Scraping corporatenepal-----------")
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
        url = response.url
        
        category = response.meta['category']
        title = response.xpath(self.title_xpath).get()
        descriptions = response.xpath(self.description_xpath).getall()
        desc = ''.join(descriptions)
        content = Utils.word_60(desc)
        img_src = response.xpath(self.image_xpath).get()
        date = response.xpath(self.date_xpath).get()
        formattedDate = Utils.techlekh_dateconverter(date)

        news = {
            'title':title.strip(),
            'content_description':content,
            'published_date':formattedDate,
            'image_url':img_src,
            'url':url,
            'category_name':category,
            'is_recent':True,
            'source_name':'techlekh'
            }
        logging.basicConfig(level=logging.INFO)
        PostNews.postnews(news)