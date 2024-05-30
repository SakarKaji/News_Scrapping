import scrapy
from Utils import Utils
from Utils import PostNews
from Utils.Constants import Standard_Category

class OnlineKhabarScrapper(scrapy.Spider):
    name = "Onlinekhabar"

    def __init__(self):
        # self.articles_xpath = '//div[@class="ok-news-post ok-post-ltr"]/a/@href'
        self.articles_xpath = "//div[@id='content']//a/@href"
        self.description_xpath = "//div[@class='ok18-single-post-content-wrap']/p/text()"
        self.title_xpath = "//h1[@class='entry-title']/text()"
        self.title_xpath2 = "//section/div/div[1]/h2/text()"
        self.title_xpath3 = "//section[1]/div/div[2]/div[1]/h1/text()"
        self.image_xpath = "//div[@class='post-thumbnail']//img/@src"
        self.date_xpath = "//div[@class='ok-title-info flx']/div[2]/span/text()"
        self.categories = {
            Standard_Category.SPORTS: r"https://www.onlinekhabar.com/sports",
            Standard_Category.SCIENCE_AND_TECHNOLOGY: r"https://www.onlinekhabar.com/content/technology-news",
            Standard_Category.BUSINESS: r"https://www.onlinekhabar.com/business",
            Standard_Category.OPINION: r"https://www.onlinekhabar.com/opinion",
            Standard_Category.ENTERTAINMENT: r"https://www.onlinekhabar.com/entertainment",
            Standard_Category.LIFESTYLE: r"https://www.onlinekhabar.com/lifestyle",
            Standard_Category.OTHERS : r"https://www.onlinekhabar.com/content/news/rastiya",
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
        url = response.url
        category = response.meta['category']
        title = response.xpath(self.title_xpath).get()
        if(title == None):
            title = response.xpath(self.title_xpath2).get()  
        if(title == None):
            title = response.xpath(self.title_xpath3).get()  
        img_src = response.xpath(self.image_xpath).get()
        descriptions = response.xpath(self.description_xpath).getall()
        desc = ''.join(descriptions)
        content = Utils.word_60(desc)
        date = response.xpath(self.date_xpath).get()
        formattedDate = Utils.online_khabar_conversion(date)   
        news = {
            'title':title,
            'content_description':content,
            'published_date':formattedDate,
            'image_url':img_src,
            'url':url,
            'category_name':category,
            'is_recent':True,
            'source_name':'onlinekhabar'
            }
        PostNews.postnews(news)
        print('----------------------------------------------------------------------------------------------------------------------------------')