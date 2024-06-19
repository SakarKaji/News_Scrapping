import scrapy
from Utils import Utils
from Utils import PostNews
from Utils.Constants import Standard_Category
from datetime import datetime
from news.article_object import article_data


class EKantipur_Scrapper(scrapy.Spider):
    name = "ekantipur"
    start_urls = ["https://ekantipur.com/"]

    def __init__(self, name: str | None = None, **kwargs: any):
        super().__init__(name, **kwargs)
        self.data = []
        self.navPath = '//ul/li[@class="nav-item "]'
        self.title_xpath = "//div[@class='article-header']/h1/text()"
        self.article_date = "//div[@class='time-author']/time/text()"
        self.description_xpath = "//div[contains(@class,'description')]//p/text()"
        self.link_xpath = "//article[@class='normal']/div[@class='teaser offset']/h2/a/@href"
        self.image_xpath = "//div[@class='description current-news-block']/div[@class='image']/figure/img/@data-src"
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

        links = response.xpath(self.link_xpath).extract()
        for link in links:
            list = link.split('/')
            date_list = list[2:5]
            date= "-".join(date_list)
            if date == self.today_date:
                each_link = "https://ekantipur.com" + link
                yield scrapy.Request( url=each_link, callback=self.scrape_each_article, meta={"link": each_link, "category": category})

    def scrape_each_article(self, response):
        category = response.meta["category"]
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
        response.meta["category"] = category_name
        news_dict = article_data(self,response,"ekantipur")
        print(f"News object :: {news_dict}")
        PostNews.postnews(news_dict)