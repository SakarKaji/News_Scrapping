
import scrapy
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews

class EnglishRatopatiScrapper(scrapy.Spider):

    name = "Ratopati"

    def __init__(self):
        self.articles_xpath = "//h3[@class]/a/@href"
        self.description_xpath = "//div[@class='content-area']/p/text()"
        self.title_xpath = "//h1[@class='news-title']/text()"
        self.image_xpath = "//div[@class='featured-images featured-images position-relative']/img/@src"
        self.date_xpath = "//div[@class='author-img flex']/div/text()[2]"
        self.categories = {
            Standard_Category.POLITICS: r"https://english.ratopati.com/category/politics",
            Standard_Category.ART: r"https://english.ratopati.com/category/arts",
            Standard_Category.SPORTS: r"https://english.ratopati.com/category/sports",
            Standard_Category.SCIENCE_AND_TECHNOLOGY: r"https://english.ratopati.com/category/science-and-technology",
            Standard_Category.SOCIETY: r"https://english.ratopati.com/category/society",
            Standard_Category.BUSINESS: r"https://english.ratopati.com/category/business",
            Standard_Category.INTERNATIONAL: r"https://english.ratopati.com/category/international",
          
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
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_article, meta={'category': response.meta['category']})


    def parse_article(self, response):
        print("--------------------------")
        url = response.url
        category = response.meta['category']
        title = response.xpath(self.title_xpath).get()
        img_src = response.xpath(self.image_xpath).get()
        descriptions = response.xpath(self.description_xpath).getall()
        desc = ''.join(descriptions)
        content = Utils.word_60(desc)
        date = response.xpath(self.date_xpath).get()
        formattedDate = Utils.RatopatiEnglish_conversion(date)

        news = {
            'title':title,
            'content_description':content,
            'published_date':formattedDate,
            'image_url':img_src,
            'url':url,
            'category_name':category,
            'is_recent':True,
            'source_name':'RatopatiEnglish'
            }
        PostNews.postnews(news)


        print(f"---------------category_name: {category},---------------------")