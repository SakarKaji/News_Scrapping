import scrapy
from Utils import Utils
from Utils import PostNews
from Utils.Constants import Standard_Category

class EKantipur_Scrapper(scrapy.Spider):
    name = "ekantipur"
    start_urls = ["https://ekantipur.com/"]

    def __init__(self, name: str | None = None, **kwargs: any):
        super().__init__(name, **kwargs)
        self.data = []
        self.navPath = '//ul/li[@class="nav-item "]'
        self.article_title = "//div[@class='article-header']/h1/text()"
        self.article_date = "//div[@class='time-author']/time/text()"
        self.article_content = "//div[contains(@class,'description current-news-block')]/p/text()"
        self.article_link = "//article[@class='normal']/div[@class='teaser offset']/h2/a/@href"
        self.image_path = "//div[@class='description current-news-block']/div[@class='image']/figure/img/@data-src"

    def parse(self, response):
        for links in response.xpath(self.navPath):
            category = links.xpath(".//a/text()").extract_first()
            category_link = links.xpath(".//a/@href").extract_first()

            if category and category_link != None:
                yield scrapy.Request(url=category_link,  callback=self.scrape_each_category, meta={"link": category_link, "category": category})

    def scrape_each_category(self, response):
        category = response.meta["category"]
        links = response.xpath(self.article_link).extract()
        count = 5
        if(count>0):
            for each_link in links:
                count -= 1
                each_link = "https://ekantipur.com" + each_link
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
        # category_mapping = {
        #     "समाचार": "others",
        #     "अर्थ / वाणिज्य": "finance",
        #     "विचार": "opinion/thoughts",
        #     "खेलकुद": "sports",
        #     "उपत्यका": "others",
        #     "मनोरञ्जन": "entertainment",
        #     "फोटोफिचर": "others",
        #     "फिचर": "others",
        #     "विश्व": "others",
        #     "ब्लग": "others",
        #     "कोसेली": "others",
        #     "प्रवास": "travel",
        #     "शिक्षा": "education",
        # }
        category_name = 'Others' if getattr(Standard_Category, response.meta['category'], None) is None else response.meta['category']

        # category = category_mapping.get(category)

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
        print(f"---------------category_name: {category},---------------------")
       

