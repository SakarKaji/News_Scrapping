
import scrapy
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews

class barakhari_scrapper(scrapy.Spider):
    name = "RisingNepal"

    def __init__(self):
        self.articleslink_xpath_breakingmain = '//*[contains(@class,"container card-shadow py-4")]//h2/a/@href'
        self.articleslink_xpath_feature = '//*[contains(@class,"blog")]//h3/a/@href'
        self.articleslink_xpath = '//*[contains(@class,"blog")]//h3/a/@href'
        # self.articleslink_xpath_container = '//div[contains(@class,"d-flex media")]/a/@href'

        self.description_xpath = '//div[contains(@class,"blog-details")]/p//text()'
        self.title_xpath = '//div[contains(@class,"text-center")]/h1/text()'
        self.image_xpath = '//div[contains(@class,"blog-banner")]/img/@src'
        self.date_xpath = '(//div[contains(@class,"d-flex align-items-center share-inline-block mb-3")])[2]//span//text()'
        self.categories = {
            Standard_Category.POLITICS: r'https://risingnepaldaily.com/categories/politics',
            Standard_Category.INTERNATIONAL: r'https://risingnepaldaily.com/categories/world',
            Standard_Category.ART: r'https://risingnepaldaily.com/categories/life-and-art',
            Standard_Category.SCIENCE_AND_TECHNOLOGY: r'https://risingnepaldaily.com/categories/science-tech',
            Standard_Category.ECONOMY: r'https://risingnepaldaily.com/categories/business',
            Standard_Category.SPORTS: r'https://risingnepaldaily.com/categories/sports',
            Standard_Category.OTHERS: r'https://risingnepaldaily.com/categories/editorial',
            Standard_Category.OPINION: r'https://risingnepaldaily.com/categories/opinion',
            Standard_Category.OTHERS: r'https://risingnepaldaily.com/categories/nation'
        }
        

    def start_requests(self):
        print("---------Scraping RisingNepal-----------")
        for category in self.categories:
            try:
                yield scrapy.Request(url=self.categories[category], callback=self.parse, meta={'category': category})
            except Exception as e:
                print(f"Error:{e}")
                continue

    def parse(self, response):
        link1 = response.xpath(self.articleslink_xpath_breakingmain).getall()
        link2 = response.xpath(self.articleslink_xpath_feature).getall()
        # link3 = response.xpath(self.articleslink_xpath_container).getall()
        link4 = response.xpath(self.articleslink_xpath).getall()
        # links = link1 + link2 + link3 + link4
        links = link1 + link2 + link4
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
        formattedDate = Utils.(date)

        news = {
            'title':title.strip(),
            'content_description':content,
            'published_date':formattedDate,
            'image_url':img_src,
            'url':url,
            'category_name':category,
            'is_recent':True,
            'source_name':'RisingNepal'
            }
        PostNews.postnews(news)

          # //*[contains(@class,"container card-shadow py-4")]//h2/a/@href
        # //*[contains(@class,"blog")]//h3/a/@href
        # //*[contains(@class,"feature")]//h4/a/@href
