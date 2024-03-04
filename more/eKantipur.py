import scrapy
from scrapy.http import Response
from bs4 import BeautifulSoup
import json
from scrapy.utils import url

class EKantipur(scrapy.Spider):
    name = "ekantipur"
    start_urls = ["https://ekantipur.com/"]

    def __init__(self, name: str | None = None, **kwargs: any):
        super().__init__(name, **kwargs)
        self.data = []
        self.article_title = "//div[@class='article-header']/h1/text()"
        self.article_body = "//div[@class='description current-news-block']"
        self.article_date = "//div[@class='time-author']/time/text()"
        self.article_link = (
            "//article[@class='normal']/div[@class='teaser offset']/h2/a/@href"
        )
        self.image_path = "//div[@class='description current-news-block']/div[@class='image']/figure/img/@data-src"

    def parse(self, response: Response):
        # print("parsing response:")
        for links in response.xpath('//ul/li[@class="nav-item "]'):

            category = links.xpath(".//a/text()").extract_first()
            category_link = links.xpath(".//a/@href").extract_first()

            if category and category_link != None:
                yield scrapy.Request(
                    url=category_link,
                    callback=self.scrape_each_category,
                    meta={"link": category_link, "category": category},
                )

        self.display()

    def display(self):
        for each in self.data:
            print(json.dumps(each, indent=4, ensure_ascii=False))

    def scrape_each_category(self, response: Response):
        category = response.meta["category"]

        links = response.xpath(self.article_link).extract()

        for each_link in links:
            each_link = "https://ekantipur.com" + each_link
            # print(f"each link : {each_link}")
            yield scrapy.Request(
                url=each_link,
                callback=self.scrape_each_article,
                meta={"link": each_link, "category": category},
            )

    def scrape_each_article(self, response: Response):
        category = response.meta["category"]

        header = response.xpath(self.article_title).extract_first()

        article_content = response.xpath(self.article_body).extract_first()
        content_soup = BeautifulSoup(article_content, "html.parser")
        article_content = content_soup.get_text()

        date = response.xpath(self.article_date).get()

        image = response.xpath(self.image_path).extract_first()

        category_mapping = {
            "समाचार": "others",
            "अर्थ / वाणिज्य": "finance",
            "विचार": "opinion/thoughts",
            "खेलकुद": "sports",
            "उपत्यका": "others",
            "मनोरञ्जन": "entertainment",
            "फोटोफिचर": "others",
            "फिचर": "others",
            "विश्व": "others",
            "ब्लग": "others",
            "कोसेली": "others",
            "प्रवास": "travel",
            "शिक्षा": "education",
        }

        category = category_mapping.get(category)

        news_dict = {
            "newspaper": "eKantipur",
            "title": header,
            "content_description": article_content,
            "image_url": image,
            "url": response.meta["link"],
            "published_date": date,
            "category": category,
        }

        self.data.append(news_dict)
        print(
            f"""
------------------------------------------------------------------------------------------------------------------------------------------
{json.dumps(news_dict, indent=4, ensure_ascii=False)}
        """
        )

        # print(
        #     f"""
        #     Newspaper  : eKantipur
        #     Cateogory  : {category}
        #     Title      : {header}
        #     Link       : {response.meta["link"]}
        #     Date       : {date}
        #     Image link : {image}
        #
        #     Content : {article_content[:255]}
        # ----------------------------------------------------------------------------------xxxxxxxxxxxxxxxxxxxxx-----------------------------------------------------------
        #     """
        # )
        #
