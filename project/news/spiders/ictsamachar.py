import scrapy
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews
import time
from urllib.parse import urljoin

class ictsamachar_scrapper(scrapy.Spider):
    name = "ictsamachar"

    def __init__(self):
        self.articles_xpath = '//section[contains(@class,"news__section")]//h3//a/@href' 
        self.description_xpath = '//div[contains(@class,"detail__description-content")]//p/text()' 
        self.title_xpath = '//div[contains(@class,"details__title-header")][1]//h1/text()' 
        self.image_xpath= '//div[contains(@class,"details__page")][1]//figure//img/@src' 
        self.date_xpath = '//div[contains(@class,"details__page")][1]//p[contains(@class,"meta post__date")]//text()[1]' 
        self.categories = {
            Standard_Category.OTHERS: r'https://ictsamachar.com/category/information/',
            Standard_Category.OTHERS: r'https://ictsamachar.com/category/news/',
            Standard_Category.OTHERS: r'https://ictsamachar.com/category/planning/',
            Standard_Category.OTHERS: r'https://ictsamachar.com/category/offer/',
            Standard_Category.OTHERS: r'https://ictsamachar.com/category/application/',
            Standard_Category.OTHERS:  r'https://ictsamachar.com/category/others/',
            Standard_Category.OTHERS:   r'https://ictsamachar.com/category/mobile/',
            Standard_Category.OTHERS: r'https://ictsamachar.com/category/laptop/',
            Standard_Category.OTHERS: r'https://ictsamachar.com/category/tv/',
            Standard_Category.OTHERS: r'https://ictsamachar.com/category/smartwatch/',
            Standard_Category.OTHERS:  r'https://ictsamachar.com/category/home-appliances/',
            Standard_Category.OTHERS:  r'https://ictsamachar.com/category/accessories/',
            Standard_Category.OTHERS:  r'https://ictsamachar.com/category/legal-fintech/',
            Standard_Category.OTHERS: r'https://ictsamachar.com/category/insurance/',
            Standard_Category.OTHERS:  r'https://ictsamachar.com/category/crime/',
            Standard_Category.OTHERS: r'https://ictsamachar.com/category/idea/',
            Standard_Category.OTHERS: r'https://ictsamachar.com/category/startup-innovation/',
            Standard_Category.OTHERS: r'https://ictsamachar.com/category/profile/',
            Standard_Category.OTHERS: r'https://ictsamachar.com/category/investment/',
            Standard_Category.OTHERS:r'https://ictsamachar.com/category/feature/',
            Standard_Category.OTHERS: r'https://ictsamachar.com/category/report/',
            Standard_Category.OTHERS: r'https://ictsamachar.com/category/education/',
            Standard_Category.OTHERS: r'https://ictsamachar.com/category/health/',
            Standard_Category.OTHERS: r'https://ictsamachar.com/category/agriculture/',
            Standard_Category.OTHERS: r'https://ictsamachar.com/category/tourism/',
            Standard_Category.OTHERS: r'https://ictsamachar.com/category/ai/',
            Standard_Category.OTHERS:r'https://ictsamachar.com/category/iot/',
            Standard_Category.OTHERS: r'https://ictsamachar.com/category/koshi/',
            Standard_Category.OTHERS:  r'https://ictsamachar.com/category/madhesh/',
            Standard_Category.OTHERS: r'https://ictsamachar.com/category/bagmati/',
            Standard_Category.OTHERS:  r'https://ictsamachar.com/category/gandaki/',
            Standard_Category.OTHERS: r'https://ictsamachar.com/category/lumbini/',
            Standard_Category.OTHERS: r'https://ictsamachar.com/category/karnali/',
            Standard_Category.OTHERS: r'https://ictsamachar.com/category/sudurpaschim/',
            Standard_Category.OTHERS: r'https://ictsamachar.com/category/conference/',
            Standard_Category.OTHERS: r'https://ictsamachar.com/category/seminar/'
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
        base_url = "https://ictsamachar.com"
        for link in links:
            if link and link.startswith("/"):  # Check if it's a relative URL    
                print(base_url+link)     
                yield scrapy.Request(url=base_url+link, callback=self.parse_article, meta={'category': response.meta['category']})


    def parse_article(self, response):
        url = response.url
        print("here")
        if url:
            category = response.meta['category']
            title = response.xpath(self.title_xpath).get()
            img_src = response.xpath(self.image_xpath).get()
            descriptions = response.xpath(self.description_xpath).getall()
            desc = ''.join(descriptions)
            content = Utils.word_60(desc)
            date = response.xpath(self.date_xpath).get()
            formattedDate = Utils.ictsamachar(date)

            if content:
                content = content.replace('\xa0', '')
            news = {
                'title':title.strip(),
                'content_description': content,
                'published_date':formattedDate,
                'image_url':img_src,
                'url':url,
                'category':category,
                'is_recent':True,
                'source':'ictsamachar'
                }
            
            print(news)
            PostNews.postnews(news)