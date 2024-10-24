
import scrapy
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews
import time

class aajakokhabar_scrapper(scrapy.Spider):
    name = "aajakokhabar"

    def __init__(self):
        self.articleslink_xpath_head = '//div[@class="category-main-content"]/h3/a/@href'
        self.articleslink_xpath = '//div[@class="thumb-content"]/h3/a/@href'
        self.description_xpath = '//div[contains(@class,"editor-box col-sm-11 col-md-11")]/p/text()'
        self.description_xpath2 = '//div[contains(@class,"change-size")]/p/text()'
        self.title_xpath = '//div[@class="detail-heads"]/h1/text()'
        self.image_xpath = '//div[@Class="details-img"]/img/@src'
        self.date_xpath = '//div[@class="details-top-left"]/ul/li[2]/text()[2]'
        self.categories = {
            Standard_Category.SOCIETY: r'https://www.aajakokhabar.com/society',
            Standard_Category.HEALTH: r'https://www.aajakokhabar.com/health',
            Standard_Category.TRAVEL: r'https://www.aajakokhabar.com/tourism',
            Standard_Category.ART: r'https://www.aajakokhabar.com/literature',
            Standard_Category.ENTERTAINMENT: r'https://www.aajakokhabar.com/entertainment',
            Standard_Category.EDUCATION: r'https://www.aajakokhabar.com/education',
            Standard_Category.ECONOMY: r'https://www.aajakokhabar.com/money-market',
            Standard_Category.SPORTS: r'https://www.aajakokhabar.com/sports',
            Standard_Category.POLITICS: r'https://www.aajakokhabar.com/politics',
            Standard_Category.OPINION: r'https://www.aajakokhabar.com/thoughts',
            Standard_Category.OTHERS: r'https://www.aajakokhabar.com/editorial'
        }
        

    def start_requests(self):
        print("---------Scraping Aajakokhabar-----------")
        for category in self.categories:
            try:
                yield scrapy.Request(url=self.categories[category], callback=self.parse, meta={'category': category})
            except Exception as e:
                print(f"Error:{e}")
                continue

    def parse(self, response):
        link1 = response.xpath(self.articleslink_xpath_head).getall()
        link2= response.xpath(self.articleslink_xpath).getall()
        links = link1 + link2
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_article, meta={'category': response.meta['category']})


    def parse_article(self, response):
        time.sleep(4)
        url = response.url
        category = response.meta['category']
        title = response.xpath(self.title_xpath).get()
        descriptions = response.xpath(self.description_xpath2).getall()
        if descriptions == None:
            descriptions = response.xpath(self.description_xpath).getall()
        desc = ''.join(descriptions)
        content = Utils.word_60(desc)
        img_src = response.xpath(self.image_xpath).get()
        date = response.xpath(self.date_xpath).get()
        formattedDate = Utils.aajakokhabar(date)

        news = {
            'title':title.strip(),
            'content_description':content.replace('\xa0', ''),
            'published_date':formattedDate,
            'image_url':img_src,
            'url':url,
            'category':category,
            'is_recent':True,
            'source':'aajakokhabar'
            }
        PostNews.postnews(news)

    