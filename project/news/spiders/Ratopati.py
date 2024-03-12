import scrapy
from Utils import Utils
from Utils import PostNews
from Utils.Constants import Standard_Category

class Ratopati_scrapper(scrapy.Spider):
    name = "Ratopati"

    def __init__(self, name: str | None = None, **kwargs: any):
        super().__init__(name, **kwargs)
        self.start_urls = 'https://www.ratopati.com/'

        self.navPath = '//nav/div/div/div[1]/ul/li'
        self.articles_path = '//div[contains(@class,"columnnews mbl-col col3")]/a/@href'
        self.articles_path_sports = '//div[contains(@class,"thumbnail-news")]/a/@href'
        self.articles_path_entertainment = '//div[@class="thumbnail-news col4"]/a/@href'
        self.article_title = "//h2[contains(@class,'heading')]/text()"
        self.article_date = "//div[@class='newsInfo']/div[@class='post-hour']/span/text()"
        self.article_content = "//div[@class='the-content']/p/text()"
        self.image_path = "//figure[@class='featured-image']/img/@src"

    def start_requests(self):
        yield scrapy.Request(url= self.start_urls, callback=self.parse)
    
    def parse(self, response):
        for link in  response.xpath(self.navPath):
            category = link.xpath(".//a/text()").get()
            category_link = link.xpath(".//a/@href").get()
            print(category_link)
            print(category)
            if category and category_link != None:
                yield scrapy.Request(url=category_link,  callback=self.scrape_each_category, meta={"category": category})

    def scrape_each_category(self, response):
        if( (response.meta['category'].strip()) == "खेलकुद"):
            links = response.xpath(self.articles_path_sports).getall()
           
        if( (response.meta['category'].strip()) == "मनोरञ्जन"):
            links = response.xpath(self.articles_path_entertainment).getall()

        if((response.meta['category'].strip()) != "मनोरञ्जन" and (response.meta['category'].strip()) != "खेलकुद"):    
            links = response.xpath(self.articles_path).getall()

        count = 5
        if(count>0):
            count = count -1
            for each_link in links: 
                yield scrapy.Request(url=each_link, callback=self.scrape_each_article, meta={"link": each_link, "category":response.meta['category']})

    def scrape_each_article(self, response):
        url = response.meta["link"] 
        category = response.meta["category"].strip()
        title = response.xpath(self.article_title).get()
        article_content = response.xpath(self.article_content).getall()
        content = ''.join(article_content)
        description = Utils.word_60(content)
        date = response.xpath(self.article_date).get()
        publishedDate = Utils.ratopati_date_conversion(date)
        image = response.xpath(self.image_path).get()
        
        category_name = 'Others' if getattr(Standard_Category, response.meta['category'], None) is None else response.meta['category']

        news = {
            "title": title,
            "content_description": description,
            "image_url": image,
            "url": url,
            "published_date": publishedDate,
            "category_name": category_name,
            'is_recent':True,
            'source_name':'ratopatinepali'
        }
        PostNews.postnews(news)
        print(f"---------------category_name: {category_name},---------------------")