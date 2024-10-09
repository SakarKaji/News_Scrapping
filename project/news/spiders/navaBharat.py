import re
import urllib
import scrapy
from datetime import datetime, timedelta

from scrapy_playwright.page import PageMethod

from Utils.Constants import Standard_Category
from Utils import Utils

from Utils import PostNews

class NavbharatTimes_Scrapper(scrapy.Spider):
    name = "navabharattimes"

    # Override default settings for storing hindi text in hindi text and not in UNICODE formay like: 
    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def __init__(self, headless=False):
        super().__init__(headless)

        self.search_page_article_card_url_xpath = '//li[@itemprop="itemListElement"]//a[@class="table_row" and @data-tn="tn"]/@href'

        self.title_xpath = "//div[@class='news_card']/h1/text()"
        self.date_xpath = '//div[@data-attr="news_card"]//span[@class="time"]/text()'
        self.date_extract_regex = r'(\d{1,2}\s\w{3,4}\s\d{4})\,\s\d{1,2}\:\d{2}.*'
        self.description_xpath = '//div[@class="story-content"]//text()[not(ancestor-or-self::*[contains(@class, "trc-content-sponsored")]) and not(ancestor-or-self::iframe)]'
        self.image_xpath = "//span[@class='_img_ads']/img/@src"

        self.base_url = f"https://navbharattimes.indiatimes.com/"
        self.keywords = ['नेपाल', 'नेपाली', 'Nepal', 'Nepali']

        self.days_for_news_recency_check = 7 #days

    def get_search_result_url(self, keyword):
        return f"{self.base_url}search?query={urllib.parse.quote_plus(keyword)}"
        
    def start_requests(self):
        for keyword in self.keywords:
            yield scrapy.Request(
                url=self.get_search_result_url(keyword), 
                callback=self.parse_search_result_page,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_load_state", "domcontentloaded"),  # Wait for HTML content to load
                    ]
                }
                
            )
    
    def parse_search_result_page(self, response):
        for news_url in response.xpath(self.search_page_article_card_url_xpath).getall():
            yield scrapy.Request(
                url=news_url, 
                callback=self.parse_an_article
            )
        
    def parse_an_article(self, response):
        date = response.xpath(self.date_xpath).get()
        match = re.findall(self.date_extract_regex, date)
        date = match[0]

        # When news is not recent
        if self.is_recent(date, days=self.days_for_news_recency_check ) == False:
            return None

        date_converted = Utils.navbharattimes_datetime(date)

        url = response.url

        title = response.xpath(self.title_xpath).get()

        img_src = response.xpath(self.image_xpath).get()

        complete_description = response.xpath(self.description_xpath).getall()
        complete_description = [des.strip() for des in complete_description]
        complete_description = ' '.join(complete_description)
        content_60words = Utils.word_60(complete_description)

        news = {
            'title':title,
            'content_description':content_60words,
            'published_date':date_converted,
            'image_url':img_src,
            'url':url,
            'category_name':Standard_Category.OTHERS,
            'is_recent':True,
            'source_id':62
        }

        PostNews.postnews_server(news)
        return news
    
    def is_recent(self, date_str, days=7) -> bool:
        """
        Check if the given date is within the specified number of days from today.

        :param date_str: Date string in the format '14 Sep 2024'
        :param days: Number of days to check for recency
        :return: True if the date is recent, False otherwise
        """
        date_obj = datetime.strptime(date_str, '%d %b %Y').date()
        today = datetime.now().date()
        threshold_date = today - timedelta(days=days)
        return date_obj >= threshold_date