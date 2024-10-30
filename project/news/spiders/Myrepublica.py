import scrapy
from Utils import Utils
from Utils import PostNews
from Utils.Constants import Standard_Category
from datetime import datetime


class Myrepublica_Scrapper(scrapy.Spider):
    name = 'Myrepublica'

    def __init__(self):
        self.start_urls = ['https://myrepublica.nagariknetwork.com/']
        self.navpath = '//ul[@class="nav navbar-nav"]/li'
        self.titlePath = '//div[@class="main-heading"]/h2/text()'
        self.imagepath = '//div[@class="inner-featured-image"]/img/@src'
        self.alt_imagepath = '//figure[@class="article__header__img"]/img/@src'
        self.contentpath = '//div[@id="newsContent"]/p/text()'
        self.datepath = '//*[@id="main-hightlight-categories-news"]/div/div/div/div[1]/div[1]/div[1]/div[1]/div/p/text()[2]'
        self.date2_path = '(//p[contains(@class,"time")]/text()[2])'
        self.next_page_xpath = "//ul[contains(@class,'pagination')]/li[last()]/a/@href"
        self.today_date = datetime.today().strftime('%Y-%m-%d')

    def start_request(self):
        yield scrapy.Request(url=self.start_urls, callback=self.parse)

    def parse(self, response):
        for links in response.xpath(self.navpath):
            href = links.css('a').attrib["href"]
            category = links.xpath('.//a/span/text()').get()
            link = 'https://myrepublica.nagariknetwork.com' + href

            print({link}, {category})
            if link and category:
                yield scrapy.Request(url=link, callback=self.parse_link, meta={'link': link, 'category': category})

    def parse_link(self, response):
        print(f"Parse Response : {response.meta}")
        full_link = 'https://myrepublica.nagariknetwork.com'

        links = response.xpath(
            '//div[contains(@class,"first-on first-list")]/h3/a/@href').getall()
        dates = response.xpath(
            '//div[contains(@class,"time")]/p/text()[2]').getall()
        if links == []:
            links = response.xpath(
                '//div[contains(@class ,"main-heading")]/a/@href').getall()
            dates = response.xpath(
                '(//p[contains(@class,"time")]/text()[2])').getall()

        for link, date in zip(links, dates):
            link = full_link + link
            date = Utils.republica_conversion(date)
            if date != self.today_date:
                break
            next_page = response.xpath(self.next_page_xpath).extract_first()
            if next_page:
                yield response.follow(next_page, self.parse_link)

            if 'category' in response.meta:
                yield scrapy.Request(url=link, callback=self.parse_article, meta={'link': link, 'category': response.meta['category']})

            else:
                response.meta['category'] = Standard_Category.OTHERS
                yield scrapy.Request(url=link, callback=self.parse_article, meta={'link': link, 'category': response.meta['category']})

    def parse_article(self, response):
        print(f"Response URL :: {response.url}, {response.meta}")
        image = response.xpath(self.imagepath).get()
        if (image == None):
            image = response.xpath(self.alt_imagepath).get()
        title = (response.xpath(self.titlePath).get()).strip()
        contentList = response.xpath(self.contentpath).getall()
        content = ''.join(contentList)
        description = Utils.word_60(content)
        date = response.xpath(self.datepath).get()
        if (date == None):
            date = response.xpath(
                '//div[@class="headline-time pull-left"]/p/text()[2]').get()
        elif (date == None):
            date = response.xpath(
                '//div[@class="article__header"]/span/text()[2]').get()

        category = response.meta['category']
        if category == "POLITICS":
            category_name = Standard_Category.POLITICS
        elif category == "ECONOMY":
            category_name = Standard_Category.ECONOMY
        elif category == "SOCIETY":
            category_name = Standard_Category.SOCIETY
        elif category == "SPORTS":
            category_name = Standard_Category.SPORTS
        elif category == "OPINION":
            category_name = Standard_Category.OPINION
        elif category == "LIFESTYLE":
            category_name = Standard_Category.LIFESTYLE
        else:
            category_name = Standard_Category.OTHERS

        publishdate = Utils.republica_conversion(date)
        news = {"title": title,
                "content_description": description,
                "image_url": image,
                "url": response.meta['link'],
                "category": category_name,
                "published_date": publishdate,
                'is_recent': True,
                'source': 'myrepublica'
                }
        PostNews.postnews(news)
