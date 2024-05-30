import scrapy
from Utils import Utils
from Utils import PostNews
from Utils.Constants import Standard_Category
from datetime import datetime

class EKantipur_Scrapper(scrapy.Spider):
    name = "ekantipur"
    start_urls = ["https://ekantipur.com/"]

    def __init__(self, name: str | None = None, **kwargs: any):
        super().__init__(name, **kwargs)
        self.data = []
        self.navPath = '//ul/li[@class="nav-item "]'
        self.article_title = "//div[@class='article-header']/h1/text()"
        self.article_date = "//div[@class='time-author']/time/text()"
        self.article_content = "//div[contains(@class,'description')]//p/text()"
        self.article_link = "//article[@class='normal']/div[@class='teaser offset']/h2/a/@href"
        self.image_path = "//div[@class='description current-news-block']/div[@class='image']/figure/img/@data-src"
        self.today_date = datetime.today().strftime('%Y-%m-%d')

    def parse(self, response):
        for links in response.xpath(self.navPath): 
            category = links.xpath(".//a/text()").extract_first()
            category_link = links.xpath(".//a/@href").extract_first()
            if category and category_link != None:
                yield scrapy.Request(url=category_link,  callback=self.scrape_each_category, meta={"link": category_link, "category": category})

    def scrape_each_category(self, response):
        links = []
        category = response.meta["category"]
        if category == "अर्थ / वाणिज्य":
            links = response.xpath('(//div[@class="bazar-layout"]//article//figure//a[1]/@href)').extract()
            for link in links:
                list = link.split('/')
                date_list = list[4:7]
                date= "-".join(date_list)
                if date == self.today_date:
                    if not link.startswith('https://'):
                        each_link = "https://ekantipur.com" + link
                        yield scrapy.Request( url=each_link, callback=self.scrape_each_article, meta={"link": each_link, "category": category})
                    yield scrapy.Request( url=link, callback=self.scrape_each_article, meta={"link": link, "category": category})

        links = response.xpath(self.article_link).extract()
        for link in links:
            list = link.split('/')
            date_list = list[2:5]
            date= "-".join(date_list)
            if date == self.today_date:
                each_link = "https://ekantipur.com" + link
                yield scrapy.Request( url=each_link, callback=self.scrape_each_article, meta={"link": each_link, "category": category})

    def scrape_each_article(self, response):
        category = response.meta["category"]
        title = response.xpath(self.article_title).extract_first()
        article_content = response.xpath(self.article_content).getall()
        content = ''.join(article_content)
        description = Utils.word_60(content)
        date = response.xpath(self.article_date).get()
        publishedDate = Utils.ekantipur_conversion(date)
        image = response.xpath(self.image_path).extract_first()
        category_mapping = {
            "समाचार": Standard_Category.OTHERS,
            "अर्थ / वाणिज्य": Standard_Category.FINANCE,
            "विचार": Standard_Category.OPINION,
            "खेलकुद": Standard_Category.SPORTS,
            "उपत्यका": Standard_Category.OTHERS,
            "मनोरञ्जन": Standard_Category.ENTERTAINMENT,
            "फोटोफिचर": Standard_Category.OTHERS,
            "फिचर": Standard_Category.OTHERS,
            "विश्व": Standard_Category.INTERNATIONAL,
            "ब्लग": Standard_Category.OTHERS,
            "कोसेली": Standard_Category.OTHERS,
            "प्रवास": Standard_Category.TRAVEL,
            "शिक्षा": Standard_Category.EDUCATION,
        }
        category_name = category_mapping[category]

        news_dict = {
            "title": title,
            "content_description": description,
            "image_url": image,
            "url": response.meta["link"],
            "published_date": publishedDate,
            "category_name": category_name,
            'is_recent':True,
            'source_name':'ekantipur'
        }
        PostNews.postnews(news_dict)