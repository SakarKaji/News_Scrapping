import scrapy
from Utils import Utils
from Utils import PostNews
from Utils.Constants import Standard_Category
from datetime import datetime
from news.article_object import article_data


class KathmanduPost_Scrapper(scrapy.Spider):
    name = "KathmanduPost"

    def __init__(self):
        self.articlelink_xpath = 'https://kathmandupost.com'
        self.title_xpath = '//h1[@style]/text()'
        self.date_xpath = '//div[@class="updated-time"]/text()'
        self.image_xpath = '//div[contains(@class,"row")]/div/img/@data-src'
        self.description_xpath = '//section/p/text()'
        self.categories = '//div[@id="myOffcanvas"]//ul[contains(@class,"list-unstyled")]/li'
        self.articles_xpath = '//article[@class="article-image "]'
        self.article_links = './/a/@href'
        self.link_xpath = './/a'
        self.next_page_xpath = "//ul[contains(@class,'pagination')]/li[last()]/a/@href"
        self.article_source = 'kathmandupost'
        self.today_date = datetime.today().strftime('%Y-%m-%d')

    def start_requests(self):
        yield scrapy.Request(url=self.articlelink_xpath, callback=self.parse)

    def parse(self, response):
        categories = response.xpath(self.categories)
        for category in categories:
            category_link = category.xpath('.//a/@href').get()
            category_text = category.xpath('.//a/text()').get()
            link = response.urljoin(category_link)
            # if category_text == " Visual Stories":
            #     break

            if category_text == "Interviews":
                break

            yield scrapy.Request(url=link, callback=self.find_article_links, meta={'category': category_text})

    def find_article_links(self, response):
        articles = response.xpath(self.articles_xpath)
        for article in articles:
            article_link = article.xpath(self.article_links).get()
            link = response.urljoin(article_link)
            break_url = link.split('/')
            new_date = break_url[4:7]
            date = '-'.join(new_date)
            if date == self.today_date:
                yield scrapy.Request(url=link, callback=self.parse_article, meta={'category': response.meta['category']})

    def parse_article(self, response):
        category = response.meta['category']

        if category == "Politics":
            category_name = Standard_Category.POLITICS

        elif category == "Opinion":
            category_name = Standard_Category.OPINION

        elif category == "Money":
            category_name = Standard_Category.FINANCE

        elif category == "Sports":
            category_name = Standard_Category.SPORTS

        elif category == "Culture & Lifestyle":
            category_name = Standard_Category.LIFESTYLE

        elif category == "Arts":
            category_name = Standard_Category.ART

        elif category == "Movies":
            category_name = Standard_Category.ENTERTAINMENT

        elif category == "Fashion":
            category_name = Standard_Category.FASHION

        elif category == "Health":
            category_name = Standard_Category.HEALTH

        elif category == "Travel":
            category_name = Standard_Category.TRAVEL

        elif category == "World":
            category_name = Standard_Category.INTERNATIONAL

        elif category == "Science & Technology":
            category_name = Standard_Category.SCIENCE_AND_TECHNOLOGY

        else:
            category_name = Standard_Category.OTHERS

        response.meta['category'] = category_name
        date = response.xpath(self.date_xpath).get()

        if date is None:
            self.formattedDate = None
        else:
            self.formattedDate = Utils.kathmandupost_conversion(date)

        news_obj = article_data(self, response)
        print(news_obj)
        PostNews.postnews(news_obj)
