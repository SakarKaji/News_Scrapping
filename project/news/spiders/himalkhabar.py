import scrapy
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews

class himalkhabar_scrapper(scrapy.Spider):
    name = "himal khabar"

    def __init__(self):
        self.articleslink_xpath_opinion = '//div[contains(@class,"bichar-content")]/a/@href'
        self.articleslink_xpath_others = '//div[contains(@class,"items")]/a/@href'
        self.articleslink_xpath_education = '//div[@class="news-break black-white sikshya-break"]/a/@href'
        self.description_xpath = '//div[contains(@class,"editor-box col-sm-11 col-md-11")]/p/text()'
        self.title_xpath = '//div[@class="title-names"]/span/text()'
        self.image_xpath = '//div[contains(@class,"featured-images lens-featured")]/figure/a/@href'
        self.date_xpath = '//span[contains(@class,"designation alt")]/text()'
        self.categories = {
            Standard_Category.OPINION: r'https://www.himalkhabar.com/bichar',
            Standard_Category.HEALTH: r'https://www.himalkhabar.com/health',
        
            Standard_Category.BUSINESS: r'https://www.himalkhabar.com/artha',
            Standard_Category.SPORTS: r'https://www.himalkhabar.com/khel',
            Standard_Category.OTHERS: r'https://www.himalkhabar.com/remittance',
            Standard_Category.EDUCATION: r'https://www.himalkhabar.com/shikshya',
            Standard_Category.SOCIETY: r'https://www.himalkhabar.com/samaj',
            Standard_Category.POLITICS: r'https://www.himalkhabar.com/raajneeti'

        }
        

    def start_requests(self):
        print("---------Scraping Himalkhabar-----------")
        for category in self.categories:
            try:
                yield scrapy.Request(url=self.categories[category], callback=self.parse, meta={'category': category})
            except Exception as e:
                print(f"Error:{e}")
                continue

    def parse(self, response):
        if(response.meta['category'] == 'opinion/thoughts'):
            links = response.xpath(self.articleslink_xpath_opinion).getall()
        
        else:
            links= response.xpath(self.articleslink_xpath_others).getall()
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
        formattedDate = Utils.himalkhabar_conversion(date)


        news = {
            'title':title.strip(),
            'content_description':content,
            'published_date':formattedDate,
            'image_url':img_src,
            'url':url,
            'category':category,
            'is_recent':True,
            'source':'himalkhabar'
            }
        print(news)
        PostNews.postnews(news)