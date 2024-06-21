import scrapy
from Utils import Utils
from Utils import PostNews
from Utils.Constants import Standard_Category
from news.article_object import article_data


class OnlineKhabarScrapper(scrapy.Spider):
    name = "Onlinekhabar"

    def __init__(self):
        # self.articles_xpath = '//div[@class="ok-news-post ok-post-ltr"]/a/@href'
        self.articlelink_xpath = "//div[@id='content']//a/@href"
        self.description_xpath = "//div[@class='ok18-single-post-content-wrap']/p/text()"
        self.title_xpath = "//h1[@class='entry-title']/text()"
        self.title_xpath2 = "//section/div/div[1]/h2/text()"
        self.title_xpath3 = "//section[1]/div/div[2]/div[1]/h1/text()"
        self.image_xpath = "//div[@class='post-thumbnail']//img/@src"
        self.date_xpath = "//div[@class='ok-title-info flx']/div[2]/span/text()"
        self.article_source = "onlinekhabar"
        self.categories = {
            Standard_Category.SPORTS: r"https://www.onlinekhabar.com/sports",
            Standard_Category.SCIENCE_AND_TECHNOLOGY: r"https://www.onlinekhabar.com/content/technology-news",
            Standard_Category.BUSINESS: r"https://www.onlinekhabar.com/business",
            Standard_Category.OPINION: r"https://www.onlinekhabar.com/opinion",
            Standard_Category.ENTERTAINMENT: r"https://www.onlinekhabar.com/entertainment",
            Standard_Category.LIFESTYLE: r"https://www.onlinekhabar.com/lifestyle",
            Standard_Category.OTHERS: r"https://www.onlinekhabar.com/content/news/rastiya",
        }

    def start_requests(self):
        for category in self.categories:
            try:
                yield scrapy.Request(url=self.categories[category], callback=self.parse, meta={'category': category})
            except Exception as e:
                print(f"Error:{e}")
                continue

    def parse(self, response):
        # links = response.xpath(self.articlelink_xpath).getall()
        links = response.css('a::attr(href)').extract()
        for link in links:
            try:
                if link.startswith('javascript:'):
                    continue

                absolute_url = response.urljoin(link)
                yield scrapy.Request(url=absolute_url, callback=self.parse_article, meta={'category': response.meta['category']})

            except Exception as e:
                print(f"Error in {link}")

    def parse_article(self, response):
        title_xpaths = [self.title_xpath, self.title_xpath2, self.title_xpath3]
        title = None

        for xpath in title_xpaths:
            extract_path = response.xpath(xpath).extract_first()
            if extract_path:
                title = extract_path.strip()
            if title:
                self.title_xpath = xpath
                break

        date = response.xpath(self.date_xpath).get()
        self.formattedDate = Utils.online_khabar_conversion(date)

        news_obj = article_data(self, response)
        PostNews.postnews(news_obj)
