
import scrapy
import time
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews


class baarakhari_scrapper(scrapy.Spider):
    name = "Baarakhari"

    def __init__(self):
        self.articleslink_xpath_breaking = '//div[contains(@class,"breaking-template feat-template")]/a/@href'
        self.articleslink_xpath_feature = '//div[contains(@class,"featured-box-item")]/a/@href'
        self.articleslink_xpath = '//div[contains(@class,"media-item")]/a/@href'
        self.articleslink_xpath_container = '//div[contains(@class,"d-flex media")]/a/@href'
        self.description_xpath = '//div[@class="editor-box"]/p/text()'
        self.title_xpath = '//div[@class="title-showcase"]/span/text()'
        self.image_xpath = '//div[@class="coverimage wp-block-image"]/img/@src'
        self.date_xpath = '//span[@class="auth-box flex-grow-1 hide-author"]/span/text()'
        self.advertisement = '//figure[@class="bigyaapan-holder"]'
        self.cross_button = '//a[@class="close_btn"]/src'
        self.categories = {
            Standard_Category.POLITICS: r'https://baahrakhari.com/politics',
            Standard_Category.INTERNATIONAL: r'https://baahrakhari.com/Immigrants',
            Standard_Category.ART: r'https://baahrakhari.com/art',
            Standard_Category.ART: r'https://baahrakhari.com/literature',
            Standard_Category.INTERNATIONAL: r'https://baahrakhari.com/international',
            Standard_Category.SCIENCE_AND_TECHNOLOGY: r'https://baahrakhari.com/technology',
            Standard_Category.ECONOMY: r'https://baahrakhari.com/economy',
            Standard_Category.SPORTS: r'https://baahrakhari.com/sport',
            Standard_Category.OTHERS: r'https://baahrakhari.com/editorial',
            Standard_Category.OPINION: r'https://baahrakhari.com/opinion',
            Standard_Category.OTHERS: r'https://baahrakhari.com/nation'

        }

    def start_requests(self):
        print("---------Scraping BARAKHARI-----------")
        for category in self.categories:
            try:
                yield scrapy.Request(url=self.categories[category], callback=self.parse, meta={'category': category})
            except Exception as e:
                print(f"Error:{e}")
                continue

    def parse(self, response):
        # Find the figure element containing the advertisement
        ad = response.xpath('//figure[@class="bigyaapan-holder"]')
        if ad:
            # Extract the anchor tag URL
            ad_url = ad.xpath('.//a/@href').get()
            # Log the ad URL
            self.logger.info(f"Found ad URL: {ad_url}")
            # "Click" or follow the ad URL by yielding a Scrapy request
            if ad_url:
                yield scrapy.Request(url=ad_url, callback=self.parse_ad)

        link1 = response.xpath(self.articleslink_xpath_breaking).getall()
        link2 = response.xpath(self.articleslink_xpath_feature).getall()
        link3 = response.xpath(self.articleslink_xpath_container).getall()
        link4 = response.xpath(self.articleslink_xpath).getall()
        links = link1 + link2 + link3+link4
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
        formattedDate = Utils.baahrakhari_conversion(date)

        news = {
            'title': title.strip(),
            'content_description': content,
            'published_date': formattedDate,
            'image_url': img_src,
            'url': url,
            'category': category,
            'is_recent': True,
            'source': 'baarakhari'
        }
        print(news)
        PostNews.postnews(news)
