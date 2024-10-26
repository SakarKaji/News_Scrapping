import scrapy
from datetime import datetime, timedelta
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews


class khabarhub_scrapper(scrapy.Spider):
    name = "khabarhub"

    def __init__(self):
        self.articleslink_xpath_main = '//h1[@class=" uk-h1"]/a/@href'
        self.articleslink_xpath = '//div[contains(@class,"uk-card-body")]/h3/a/@href'
        self.articleslink_xpath_other = '//div[@class="uk-overlay uk-position-bottom uk-light uk-animation-slide-bottom uk-animation-reverse"]/h3/a/@href'
        self.articleslink_xpath_sports = '//h3[@class="uk-card-title ah-recent"]/a/@href'

        self.description_xpath = '//div[contains(@class,"post-entry")]/p/span/text()'
        self.description_xpath_2 = '//div[contains(@class,"post-entry")]/p/text()'

        self.title_xpath = '//h1[@class="single-title"]/text()'
        self.image_xpath = '//div[@class="banner-top uk-text-center uk-background-muted uk-margin-small-bottom"]/img/@src'
        self.date_xpath = '//p[@class="single-date"]/text()'
        self.categories = {
            # falls under articleslink_xpath_main + xpath
            Standard_Category.POLITICS: r'https://khabarhub.com/category/%e0%a4%b0%e0%a4%be%e0%a4%9c%e0%a4%a8%e0%a5%80%e0%a4%a4%e0%a4%bf/',
            Standard_Category.LIFESTYLE: r'https://khabarhub.com/category/%e0%a4%9c%e0%a5%80%e0%a4%b5%e0%a4%a8%e0%a4%b6%e0%a5%88%e0%a4%b2%e0%a5%80/',
            Standard_Category.OTHERS: r'https://khabarhub.com/category/%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%B5%E0%A4%BE%E0%A4%B8/',
            Standard_Category.OPINION: r'https://khabarhub.com/category/%e0%a4%b5%e0%a4%bf%e0%a4%9a%e0%a4%be%e0%a4%b0/',
            Standard_Category.ART: r'https://khabarhub.com/category/%e0%a4%b8%e0%a4%be%e0%a4%b9%e0%a4%bf%e0%a4%a4%e0%a5%8d%e0%a4%af/',
            # below falls under xpath other
            Standard_Category.ENTERTAINMENT: r'https://khabarhub.com/category/%e0%a4%ae%e0%a4%a8%e0%a5%8b%e0%a4%b0%e0%a4%9e%e0%a5%8d%e0%a4%9c%e0%a4%a8/',
            Standard_Category.HEALTH: r'https://khabarhub.com/category/%e0%a4%b8%e0%a5%8d%e0%a4%b5%e0%a4%be%e0%a4%b8%e0%a5%8d%e0%a4%a5%e0%a5%8d%e0%a4%af/',
            Standard_Category.SCIENCE_AND_TECHNOLOGY: r'https://khabarhub.com/category/%e0%a4%b8%e0%a5%82%e0%a4%9a%e0%a4%a8%e0%a4%be-%e0%a4%aa%e0%a5%8d%e0%a4%b0%e0%a4%b5%e0%a4%bf%e0%a4%a7%e0%a4%bf/',
            Standard_Category.TRAVEL: r'https://khabarhub.com/category/%e0%a4%9f%e0%a5%8d%e0%a4%b0%e0%a4%be%e0%a4%ad%e0%a4%b2/',
            # these falls under sports xpath
            Standard_Category.SPORTS: r'https://khabarhub.com/category/%e0%a4%96%e0%a5%87%e0%a4%b2%e0%a4%95%e0%a5%81%e0%a4%a6/',
            Standard_Category.SCIENCE_AND_TECHNOLOGY: r'https://khabarhub.com/category/%e0%a4%b8%e0%a5%82%e0%a4%9a%e0%a4%a8%e0%a4%be-%e0%a4%aa%e0%a5%8d%e0%a4%b0%e0%a4%b5%e0%a4%bf%e0%a4%a7%e0%a4%bf/',
            Standard_Category.OTHERS: r'https://khabarhub.com/category/%e0%a4%b8%e0%a5%81%e0%a4%b0%e0%a4%95%e0%a5%8d%e0%a4%b7%e0%a4%be/'
        }

    def start_requests(self):
        print("---------Scraping khabarhub-----------")
        for category in self.categories:
            try:
                yield scrapy.Request(url=self.categories[category], callback=self.parse, meta={'category': category})
            except Exception as e:
                print(f"Error:{e}")
                continue

    def parse(self, response):

        links1 = response.xpath(self.articleslink_xpath).getall()
        link2 = response.xpath(self.articleslink_xpath_main).getall()
        links = links1 + link2
        if len(links) == 0:
            links = response.xpath(self.articleslink_xpath_sports).getall()
        if len(links) == 0:
            links = response.xpath(self.articleslink_xpath_other).getall()

        for link in links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_article, meta={'category': response.meta['category']})

    def parse_article(self, response):
        date = response.xpath(self.date_xpath).get()
        formattedDate = Utils.khaburhub_dateconverter(date)
        five_days_ago = datetime.now() - timedelta(days=5)
        if formattedDate and (datetime.strptime(formattedDate, "%Y-%m-%d") >= five_days_ago):
            url = response.url
            category = response.meta['category']
            title = response.xpath(self.title_xpath).get()
            descriptions = response.xpath(self.description_xpath_2).getall()
            if (not descriptions or len(descriptions) == 0):
                descriptions = response.xpath(self.description_xpath).getall()

            desc = ''.join(descriptions)
            content = Utils.word_60(desc)
            img_src = response.xpath(self.image_xpath).get()

            news = {
                'title': title.strip(),
                'content_description': content,
                'published_date': formattedDate,
                'image_url': img_src,
                'url': url,
                'category': category,
                'is_recent': True,
                'source': 'khabarhub'
            }
            print(news)
            PostNews.postnews(news)
