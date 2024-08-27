import scrapy
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews
import logging
import time
from lxml import html


class lokantar_scrapper(scrapy.Spider):
    name = "lokantar"

    def __init__(self):
        self.articleslink_xpath_main = '//div[@class="horizontal-main-grid-content"]/a/@href'
        self.articleslink_xpath = '//div[@class="simple-grid-section-content"]/div/a/@href'
        self.description_xpath = '//div[@class="detail-content"]/div/p/text()'
        self.title_xpath = 'normalize-space(//div[@class="detail-content-title"]/h1)'
        self.image_xpath = '//div[@class="col-lg-12 col-md-12"]/img/@src'
        self.date_xpath = '//div[@class="detail-content-location-date mt-2 "]//p'
        self.categories = {
            Standard_Category.OTHERS: r'https://www.lokaantar.com/category/khoj',
            Standard_Category.OTHERS: r'https://www.lokaantar.com/category/feature',
            Standard_Category.OTHERS: r'https://www.lokaantar.com/category/agralekh',

            Standard_Category.OTHERS: r'https://www.lokaantar.com/category/interview',
            Standard_Category.OTHERS: r'https://www.lokaantar.com/category/aalekh',
            Standard_Category.OTHERS: r'https://www.lokaantar.com/category/tippani',



            Standard_Category.ENTERTAINMENT: r'https://www.lokaantar.com/category/cinema',
            Standard_Category.ENTERTAINMENT: r'https://www.lokaantar.com/category/music',
            Standard_Category.ART: r'https://www.lokaantar.com/category/literature',
            Standard_Category.BUSINESS: r'https://www.lokaantar.com/category/consumers',
            Standard_Category.ECONOMY: r'https://www.lokaantar.com/category/bank-share',
            Standard_Category.ECONOMY: r'https://www.lokaantar.com/category/economy',
            Standard_Category.HEALTH: r'https://www.lokaantar.com/category/health',
            Standard_Category.LIFESTYLE: r'https://www.lokaantar.com/category/jiban-darshan',
            Standard_Category.INTERNATIONAL: r'https://www.lokaantar.com/category/international',
            Standard_Category.OTHERS: r'https://www.lokaantar.com/category/governance',
            Standard_Category.SPORTS: r'https://www.lokaantar.com/category/sports',
            Standard_Category.POLITICS: r'https://www.lokaantar.com/category/politics'
        }

    def start_requests(self):
        for category in self.categories:
            try:
                print(f"Category :: {category}")
                yield scrapy.Request(url=self.categories[category], callback=self.parse, meta={'category': category})
            except Exception as e:
                print(f"Error:{e}")
                continue

    def parse(self, response):
        print(response.url)
        link1 = response.xpath(self.articleslink_xpath_main).getall()
        link2 = response.xpath(self.articleslink_xpath).getall()
        links = link1 + link2
        for link in links:
            try:
                print(f"Link :: {response.urljoin(link)}")
                yield scrapy.Request(url=response.urljoin(link), callback=self.parse_article, meta={'category': response.meta['category']})

            except Exception as e:
                print(f"Error in link {link}")

    def parse_article(self, response):
        time.sleep(5)
        url = response.url
        category = response.meta['category']
        title_xpaths = [self.title_xpath]
        title = None

        for xpath in title_xpaths:
            extract_path = response.xpath(xpath).extract_first()
            if extract_path:
                title = extract_path.strip()
            if title:
                self.title_xpath = xpath
                break

        title = response.xpath(self.title_xpath).get()
        print(f"Title :: {title}")
        descriptions = response.xpath(self.description_xpath).getall()
        desc = ''.join(descriptions)
        content = Utils.word_60(desc)
        img_src = response.xpath(self.image_xpath).get()
        date_string = response.xpath(self.date_xpath).get()
        # Convert the string to an lxml element
        p_element = html.fromstring(date_string)

        # Extract the text content of the <span> elements
        spans = p_element.xpath('.//span/text()')
        print(f"Spans: {spans}")
        # Determine the date string based on the number of <span> elements
        if len(spans) == 2:
            date = spans[1]  # Take the second <span> if there are two
        elif len(spans) == 1:
            # Take the first <span> if there is only one
            date = spans[0]
        else:
            date = None

        formattedDate = Utils.lokaantar_conversion(date)

        news = {
            'title': title.strip(),
            'content_description': content,
            'published_date': formattedDate,
            'image_url': img_src,
            'url': url,
            'category_name': category,
            'is_recent': True,
            'source_name': 'lokaantar'
        }
        logging.basicConfig(level=logging.INFO)
        PostNews.postnews(news)
