import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime
from time import sleep
import random

class HimalayanScraper(scrapy.Spider):
    name = "himalayan_category"
    # custom_settings = {
    #     'DOWNLOAD_DELAY': 5,
    #     'CONCURRENT_REQUESTS_PER_DOMAIN': 16,
    #     'CONCURRENT_REQUESTS_PER_IP': 16,
    #     'AUTOTHROTTLE_ENABLED': True,
    #     'AUTOTHROTTLE_START_DELAY': 5,

    # }

    def __init__(self):
        self.news = []
        print("Crawling Himalayan Times")
        self.articles_xpath='.//div[@class="ht-homepage-left-articles  "]/div[@class="js animate-box mainWidget"]/div[@class="row"]/div[@class="col-sm-6"]'
        self.link_xpath='.//a'
        self.xpath_article='//article[contains(@class,"articleDetails")]'
        self.title_xpath='//h1[@class="alith_post_title"]/text()'
        self.date_xpath='//div[@class="article_date"]/text()'
        self.desc_xpath='//div[@class="dropcap column-1 animate-box"]/p/text()'
        self.img_xpath='//div[@class="articleImg"]/figure[@class=" relative"]/div[@class="layout-ratio"]/picture/source'

    def start_requests(self):
        self.Categories = [
            "business",
            "sports",
            "lifestyle",
            "entertainment",
            "science and technology",
            "politics",
            "international",
            "world",
            "travel",
            "fashion",
            "education",
            "finance",
            "art",
            "economy",
            "opinion",
            "thoughts",
            "society",
            "health",
            "weather",
            "others"]

        self.urls = {'kathmandu': 'https://thehimalayantimes.com/kathmandu/',
                     'nepal': 'https://thehimalayantimes.com/nepal/',
                     'world': 'https://thehimalayantimes.com/world/',
                     'opinion': 'https://thehimalayantimes.com/opinion/',
                     'business': 'https://thehimalayantimes.com/business/',
                     'sports': 'https://thehimalayantimes.com/sports/',
                     'entertainment': 'https://thehimalayantimes.com/entertainment/',
                     'lifestyle': 'https://thehimalayantimes.com/lifestyle/',
                     'science and technology': 'https://thehimalayantimes.com/science-and-tech/',
                     'environment': 'https://thehimalayantimes.com/environment/',
                     'health': 'https://thehimalayantimes.com/health/',
                    }

        for category, url in self.urls.items():
            try:
                category = category if category in self.Categories else 'others'
                yield scrapy.Request(url=url, callback=self.parse, meta={'url': url, 'categories': category})
                t=random.randint(1, 5)
                sleep(t)
            except Exception as e:
                print(f"Error:{e}")
                continue

    def parse(self, response):
        print("*********************************")
        print(f"URL:{response.url}")
        print(f"Category:{response.meta['categories']}")
        print("*********************************")
        articles = response.xpath(self.articles_xpath)

        for article in articles:
            link = article.xpath(self.link_xpath).attrib['href']
            print(f"Link:{link}")
            yield scrapy.Request(url=link, callback=self.parse_article,meta={'categories': response.meta['categories']})
            t=random.randint(1, 5)
            sleep(t)

    def parse_article(self, response):
        article = response.xpath(self.xpath_article)
        # print(f"Article:{article}")
        title = article.xpath(self.title_xpath).get().strip()
        # print(f"Title:{title}")
        article_date = article.xpath(self.date_xpath).get()
        # print(f"Date:{article_date}")
        date_object = datetime.strptime(article_date, ' Published: %I:%M %p %b %d, %Y  ')
        formatted_date = date_object.strftime('%Y-%m-%d')

        try:
            # desc = article.xpath('//div[@class="dropcap column-1 animate-box"]/text()').getall()
            all = article.xpath(self.desc_xpath).getall()
            description = ''
            for i in all:
                description += i.strip()
        except:
            description = None
            print("error in description")

        try:
            img_src = article.xpath(self.img_xpath).attrib['data-srcset']
        except:
            img_src = None
        
        try:
            item = {'title': title, 'content_description': description, 'published_date': formatted_date, 'image_url': img_src,
                'url': response.url, 'newspaper': 'The Himalayan Times', 'category_name': response.meta['categories']}
            self.news.append(item)

        except Exception as e:
            print(f"Error:{e}")
            pass   

    def closed(self,response):
        print("Crawling Complete")
        for item in self.news:
            print("*********************************")
            print(item)
            print("*********************************")
