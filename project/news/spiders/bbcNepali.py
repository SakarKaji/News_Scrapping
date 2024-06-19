import scrapy
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews

class bbcNepali_scrapper(scrapy.Spider):
    name = "bbcNepali"
 
    def __init__(self):
        self.start_urls = 'https://www.bbc.com/nepali'
        self.articles_xpath = '//div/div/section[1]/div/ul//h3[@class="bbc-1kr00f0 e47bds20"]/a/@href'
        self.description_xpath = '//*[@id="main-wrapper"]/div/div/div/div[1]/main/div/p/text()'
        self.title_xpath = '//*[@id="content"]/text()'
        self.image_xpath = '//div/div/div/div[1]/main/figure[1]/div/picture/img/@src'
        self.date_xpath = '//div/div/div/div[1]/main/div[2]/time/@datetime'
        
    def start_requests(self):
        yield scrapy.Request(url=self.start_urls, callback=self.parse)
         

    def parse(self, response):
        for link in response.xpath(self.articles_xpath).getall():
            yield scrapy.Request(url=link, callback=self.parse_article)

    def parse_article(self, response):
        url = response.url
        title = (response.xpath(self.title_xpath).get()).strip()
        img_src = response.xpath(self.image_xpath).get()
        descriptions = response.xpath(self.description_xpath).getall()
        desc = ''.join(descriptions)
        content = Utils.word_60(desc)
        date = response.xpath(self.date_xpath).get()
        news = {
            'title':title.strip(),
            'content_description':content,
            'published_date':date,
            'image_url':img_src,
            'url':url,
            'category_name':Standard_Category.OTHERS,
            'is_recent':True,
            'source_name':'bbcnepali'
            }
        PostNews.postnews(news)
