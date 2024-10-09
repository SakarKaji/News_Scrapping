import re
import scrapy
from datetime import datetime, timedelta

from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews


class TimesOfIndia_Scrapper(scrapy.Spider):
    name = "timesofindia"

    def __init__(self):
        self.search_page_article_card_url_xpath = "//div[contains(@class, 'uwU81')]/a/@href"

        self.title_xpath = "//h1[@class='HNMDR']//text()"
        self.date_xpath = "//div[@class='xf8Pm byline']/span/text()"
        self.date_extract_regex = r'.*U?p?d?a?t?e?d?\:?\s?(\w{3,4}\s\d{1,2}\,\s\d{4})\,\s\d{2}\:\d{2}.*'
        self.description_xpath = "(//div[@class='_s30J clearfix  '])[1]//text()[not(ancestor-or-self::*[@id='poll-widget']) and not(ancestor-or-self::div[@class='mgid_second_mrec_parent'])]"
        self.image_xpath = "(//div[@class='wJnIp'])[1]/img/@src"

        self.base_url = f"https://timesofindia.indiatimes.com"
        self.keywords = ['nepal', 'nepali']

        self.days_for_news_recency_check = 7  # days

    def get_search_result_url(self, keyword):
        url = self.base_url
        url = f"{url}/topic/{keyword}"
        return url

    def start_requests(self):
        for keyword in self.keywords:
            yield scrapy.Request(
                url=self.get_search_result_url(keyword),
                callback=self.parse_search_result_page
            )

    def parse_search_result_page(self, response):
        article_links = response.xpath(
            self.search_page_article_card_url_xpath).getall()
        for article_link in article_links:
            yield scrapy.Request(url=article_link, callback=self.parse_an_article)

    def parse_an_article(self, response):

        date = response.xpath(self.date_xpath).get()
        match = re.findall(self.date_extract_regex, date)
        date = match[0]

        # When news is not recent
        if self.is_recent(date, days=self.days_for_news_recency_check) == False:
            return None

        date_converted = Utils.timesofindia_datetime(date)

        url = response.url

        title = response.xpath(self.title_xpath).get()

        img_src = response.xpath(self.image_xpath).get()

        complete_description = response.xpath(self.description_xpath).getall()
        complete_description = [des.strip() for des in complete_description]
        complete_description = ' '.join(complete_description)
        content_60words = Utils.word_60(complete_description)

        # Parse the date string into a datetime object
        date_obj = datetime.strptime(date_converted, '%B %d, %Y')
        # Format the datetime object into 'yyyy-mm-dd'
        formatted_date = date_obj.strftime('%Y-%m-%d')

        news = {
            "title": title,
            "content_description": content_60words,
            "published_date": formatted_date,
            "image_url": img_src,
            "url": url,
            "category_name": Standard_Category.OTHERS,
            "is_recent": True,
            "source_id": 46
        }
        PostNews.postnews_server(news)

    def is_recent(self, date_str, days=7) -> bool:
        """
        Check if the given date is within the specified number of days from today.

        :param date_str: Date string in the format 'Sep 5, 2024'
        :param days: Number of days to check for recency
        :return: True if the date is recent, False otherwise
        """
        date_obj = datetime.strptime(date_str, '%b %d, %Y').date()
        today = datetime.now().date()
        threshold_date = today - timedelta(days=days)
        return date_obj >= threshold_date


# import scrapy
# from Utils.Constants import Standard_Category
# from Utils import Utils
# from Utils import PostNews
# import time
# class timesofindia_scrapper(scrapy.Spider):
#     name = "timesofindia"

#     def __init__(self):
#         self.articles_xpath = '//div[@class="col_l_2 col_m_3"]//figure/a/@href'
#         self.description_xpath = '//div[@class="_s30J clearfix  "]/text()'
#         self.title_xpath = '//h1[@class="HNMDR"]/span/text()'
#         self.image_xpath = '//div[@class="wJnIp"]/img/@src'
#         self.date_xpath = '//div[@class="published-date col-md-6"]/span/text()[1]'
#         self.date_xpath_2 = '//div[@class="xf8Pm byline"]/span/text()'
#         self.categories = {
#             Standard_Category.SPORTS: r"https://timesofindia.indiatimes.com/sports",
#             Standard_Category.OTHERS: r"https://timesofindia.indiatimes.com/india",
#             Standard_Category.INTERNATIONAL: r'https://timesofindia.indiatimes.com/world',
#             Standard_Category.ENTERTAINMENT: r'https://timesofindia.indiatimes.com/etimes',
#             Standard_Category.SCIENCE_AND_TECHNOLOGY: r'https://timesofindia.indiatimes.com/technology',
#             Standard_Category.SCIENCE_AND_TECHNOLOGY: r'https://timesofindia.indiatimes.com/auto',
#             Standard_Category.BUSINESS: r'https://timesofindia.indiatimes.com/business',
#             Standard_Category.EDUCATION: r'https://timesofindia.indiatimes.com/education',
#         }


#     def start_requests(self):
#         for category in self.categories:
#             try:
#                 yield scrapy.Request(url=self.categories[category], callback=self.parse, meta={'category': category})
#             except Exception as e:
#                 print(f"Error:{e}")
#                 continue

#     def parse(self, response):
#         links= response.xpath(self.articles_xpath).getall()
#         for link in links:
#             yield scrapy.Request(url=link, callback=self.parse_article, meta={'category': response.meta['category']})


#     def parse_article(self, response):
#         time.sleep(3)
#         url = response.url
#         category = response.meta['category']
#         title = response.xpath(self.title_xpath).extract_first()
#         img_src = response.xpath(self.image_xpath).extract_first()
#         descriptions = response.xpath(self.description_xpath).getall()
#         desc = ''.join(descriptions)
#         content = Utils.word_60(desc)
#         date = response.xpath(self.date_xpath).get()
#         if date == None:
#             date = response.xpath(self.date_xpath_2).get()
#         formattedDate = Utils.time_of_india_date_convertor1(date)
#         news = {
#             'title':title.strip(),
#             'content_description':content,
#             'published_date':formattedDate,
#             'image_url':img_src,
#             'url':url,
#             'category_name':category,
#             'is_recent':True,
#             'source_name':'timesofindia'
#             }
#         PostNews.postnews(news)


# import scrapy
# from Utils.Constants import Standard_Category
# from Utils import Utils
# from Utils import PostNews
# import time
# class timesofindia_scrapper(scrapy.Spider):
#     name = "timesofindia"

#     def __init__(self):
#         self.articles_xpath = '//div[@class="col_l_2 col_m_3"]//figure/a/@href'
#         self.description_xpath = '//div[@class="_s30J clearfix  "]/text()'
#         self.title_xpath = '//h1[@class="HNMDR"]/span/text()'
#         self.image_xpath = '//div[@class="wJnIp"]/img/@src'
#         self.date_xpath = '//div[@class="published-date col-md-6"]/span/text()[1]'
#         self.date_xpath_2 = '//div[@class="xf8Pm byline"]/span/text()'
#         self.categories = {
#             Standard_Category.SPORTS: r"https://timesofindia.indiatimes.com/sports",
#             Standard_Category.OTHERS: r"https://timesofindia.indiatimes.com/india",
#             Standard_Category.INTERNATIONAL: r'https://timesofindia.indiatimes.com/world',
#             Standard_Category.ENTERTAINMENT: r'https://timesofindia.indiatimes.com/etimes',
#             Standard_Category.SCIENCE_AND_TECHNOLOGY: r'https://timesofindia.indiatimes.com/technology',
#             Standard_Category.SCIENCE_AND_TECHNOLOGY: r'https://timesofindia.indiatimes.com/auto',
#             Standard_Category.BUSINESS: r'https://timesofindia.indiatimes.com/business',
#             Standard_Category.EDUCATION: r'https://timesofindia.indiatimes.com/education',
#         }


#     def start_requests(self):
#         for category in self.categories:
#             try:
#                 yield scrapy.Request(url=self.categories[category], callback=self.parse, meta={'category': category})
#             except Exception as e:
#                 print(f"Error:{e}")
#                 continue

#     def parse(self, response):
#         links= response.xpath(self.articles_xpath).getall()
#         for link in links:
#             yield scrapy.Request(url=link, callback=self.parse_article, meta={'category': response.meta['category']})


#     def parse_article(self, response):
#         time.sleep(3)
#         url = response.url
#         category = response.meta['category']
#         title = response.xpath(self.title_xpath).extract_first()
#         img_src = response.xpath(self.image_xpath).extract_first()
#         descriptions = response.xpath(self.description_xpath).getall()
#         desc = ''.join(descriptions)
#         content = Utils.word_60(desc)
#         date = response.xpath(self.date_xpath).get()
#         if date == None:
#             date = response.xpath(self.date_xpath_2).get()
#         formattedDate = Utils.time_of_india_date_convertor1(date)
#         news = {
#             'title':title.strip(),
#             'content_description':content,
#             'published_date':formattedDate,
#             'image_url':img_src,
#             'url':url,
#             'category_name':category,
#             'is_recent':True,
#             'source_name':'timesofindia'
#             }
#         PostNews.postnews(news)
