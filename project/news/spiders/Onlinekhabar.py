import scrapy
from Utils import Utils
from Utils import PostNews
from Utils.Constants import Standard_Category
from news.article_object import article_data


class OnlineKhabarScrapper(scrapy.Spider):
    name = "Onlinekhabar"

    def __init__(self):
        self.articlelink_xpath = '//section[contains(@class,"ok-bises")]//a/@href'
        self.articlelink2_xpath = '//section[contains(@class,"ok-section-mukhya")]//a/@href'
        self.title_xpath = '//div[@class="ok-post-title-right"]/h1/text()'
        self.title_xpath2 = '//div[@class="single-post-heading"]/h1/text()'
        self.title_xpath3 = '//div[@class=" post-title-wrap"]/h4/a/text()'
        self.imagepath = '//div[@class="post-thumbnail"]/img/@src'
        self.paragraphpath = '//div[contains(@class,"content")]//p/text()'
        self.content = '//div[contains(@class,"content")]/p'
        self.datepath = '//div[@class="ok-post-title-right"]/div[@class="ok-title-info flx"]/div[@class="ok-news-post-hour"]/span/text()'
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
        try:
            url = response.url
            print(f"URL :: {url}")
            title_xpaths = [self.title_xpath,
                            self.title_xpath2,
                            self.title_xpath3]
            title = None

            for xpath in title_xpaths:
                extract_path = response.xpath(xpath).extract_first()
                if extract_path:
                    title = extract_path.strip()
                    break
            print(f"Title :: {title}")

            image = response.xpath(self.imagepath).get()
            paragraph = response.xpath(self.paragraphpath).getall()
            content = ''.join(paragraph)
            date = response.xpath(self.datepath).get()
            category = response.meta['category']

            try:
                published_date = Utils.online_khabar_conversion(date)
            except:
                published_date = Utils.nepali_date_today()

            unwanted_chars = ['\xa0', '\n', '\u202f', '\u200d']
            for char in unwanted_chars:
                content = content.replace(char, '')
            news = {
                "title": title,
                "content_description": Utils.word_60(content),
                "published_date": published_date,
                "url": url,
                "category": category,
                "source": 'onlinekhabar'
            }
            if image:
                news["image_url"] = image
            PostNews.postnews(news)
        except Exception as e:
            print(f"errror received in others_news {e}")
