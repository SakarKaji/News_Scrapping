import scrapy
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews

class Merolagani_scrapper(scrapy.Spider):
    name = "merolagani"

    def __init__(self):
        self.articles_xpath = '//div[@class="col-sm-6"]//a/@href'
        self.description_xpath = '//div[@class="media-body"]/div/p/span/text()'
        self.title_xpath = '//h4[@class="media-title newsTitle"]/text()'
        self.image_xpath = '//div[@class="col-sm-6"]//a/img/@src'
        self.date_xpath = '//span[@id="ctl00_ContentPlaceHolder1_newsDate"]/text()'
        self.start_urls = 'https://merolagani.com/NewsList.aspx'
        self.categories = {
            Standard_Category.OPINION: r"https://merolagani.com/NewsList.aspx?id=10&type=latest",
            Standard_Category.SCIENCE_AND_TECHNOLOGY: r'https://merolagani.com/NewsList.aspx?id=23&type=latestY',
            Standard_Category.INTERNATIONAL: r'https://merolagani.com/NewsList.aspx?id=12&type=latest',
            Standard_Category.ECONOMY: r'https://merolagani.com/NewsList.aspx?id=13&type=latest',
            Standard_Category.ECONOMY: r'https://merolagani.com/NewsList.aspx?id=15&type=latest',
            Standard_Category.BUSINESS: r'https://merolagani.com/NewsList.aspx?id=12&type=latest',
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
        images = response.xpath(self.image_xpath).getall()
        for link, image in zip(links, images):
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_article, meta={'image': image, 'category':response.meta['category']})

    def parse_article(self, response):
        url = response.url
        img_src =  response.meta['image']
        category =  response.meta['category']
        title = response.xpath(self.title_xpath).get()       
        descriptions = response.xpath(self.description_xpath).getall()
        desc = ''.join(descriptions)
        content = Utils.word_60(desc)
        date = response.xpath(self.date_xpath).get()
        formattedDate = Utils.mero_lagani_conversion(date)
        news = {
            'title':title.strip(),
            'content_description':content,
            'published_date':formattedDate,
            'image_url':img_src,
            'url':url,
            'category_name':category,
            'is_recent':True,
            'source_name':'merolagani'
            }
        PostNews.postnews(news)
