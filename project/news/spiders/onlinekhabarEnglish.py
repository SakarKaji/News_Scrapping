import scrapy
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews

class OnlinekhabarEnglish_scrapper(scrapy.Spider):
    name = "englishonlinekhabar"

    def __init__(self):
        self.articleslink_xpath = '//div[contains(@class,"ok-post-contents")]/h2/a/@href'
        self.description_xpath = '//div[contains(@class,"post-content-wrap")]/p/text()'
        self.title_xpath = '//div[contains(@class,"ok-post-header")]/h1/text()'
        self.image_xpath = '//figure[contains(@class,"wp-block-image size-full")]/img/@src'
        self.date_xpath = '//span[contains(@class,"ok-post-date")]/text()'
        self.categories = {
            Standard_Category.SPORTS: r"https://english.onlinekhabar.com/category/sports",
            Standard_Category.TRAVEL: r'https://english.onlinekhabar.com/category/travel',
            Standard_Category.LIFESTYLE: r'https://english.onlinekhabar.com/category/lifestyle',
            Standard_Category.ECONOMY: r'https://english.onlinekhabar.com/category/economy',
            Standard_Category.POLITICS: r'https://english.onlinekhabar.com/category/political',
            Standard_Category.SCIENCE_AND_TECHNOLOGY: r'https://english.onlinekhabar.com/category/technology',
            Standard_Category.OPINION: r'https://english.onlinekhabar.com/category/opinion',
            Standard_Category.ENTERTAINMENT: r'https://english.onlinekhabar.com/category/entertainment',
        }
        

    def start_requests(self):
        for category in self.categories:
            try:
                yield scrapy.Request(url=self.categories[category], callback=self.parse, meta={'category': category})
            except Exception as e:
                print(f"Error:{e}")
                continue

    def parse(self, response):
        links= response.xpath(self.articleslink_xpath).getall()
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
        formattedDate = Utils.english_online_khabar_datetime(date)

        news = {
            'title':title.strip(),
            'content_description':content,
            'published_date':formattedDate,
            'image_url':img_src,
            'url':url,
            'category':category,
            'is_recent':True,
            'source':'englishonlinekhabar'
            }
        print(news)
        PostNews.postnews(news)
