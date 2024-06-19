import scrapy
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews

class corporatenepal_scrapper(scrapy.Spider):
    name = "corporatenepal"

    def __init__(self):
        self.articleslink_xpath = '//div[@class="mb-10 match-2"]/h5/a/@href'
        self.description_xpath = '//div[@class="detail-news-details-paragh detail-fontsize text-justify mb-30"]/p/text()'
        self.title_xpath = '//div[@class="heading-title-50 mb-15"]/h1/a/text()'
        self.image_xpath = '//div[@class="post mb-30"]/a[@class="post-img"]/img/@src'
        self.date_xpath = '//span[@class="post-date-grey"]/text()'
        self.categories = {
            Standard_Category.OPINION: r'https://www.corporatenepal.com/category/politics',
            Standard_Category.SOCIETY: r'https://www.corporatenepal.com/category/society',
            Standard_Category.INTERNATIONAL: r'https://www.corporatenepal.com/category/world',
            Standard_Category.SPORTS: r'https://www.corporatenepal.com/category/sports',
            Standard_Category.INTERNATIONAL: r'https://www.corporatenepal.com/category/migrant',
            Standard_Category.BUSINESS: r'https://www.corporatenepal.com/category/industry',
            Standard_Category.ECONOMY: r'https://www.corporatenepal.com/category/finance',
            Standard_Category.ECONOMY: r'https://www.corporatenepal.com/category/market',
            Standard_Category.SCIENCE_AND_TECHNOLOGY: r'https://www.corporatenepal.com/category/tech',
            Standard_Category.OPINION: r'https://www.corporatenepal.com/category/view',
            Standard_Category.HEALTH: r'https://www.corporatenepal.com/category/health',
            Standard_Category.OPINION: r'https://www.corporatenepal.com/category/interview',
            Standard_Category.OTHERS: r'https://www.corporatenepal.com/category/horoscope',

            Standard_Category.OTHERS: r'https://www.corporatenepal.com/category/jobs'
        }
        

    def start_requests(self):
        print("---------Scraping corporatenepal-----------")
        for category in self.categories:
            try:
                yield scrapy.Request(url=self.categories[category], callback=self.parse, meta={'category': category})
            except Exception as e:
                print(f"Error:{e}")
                continue

    def parse(self, response):

        links = response.xpath(self.articleslink_xpath).getall()

        for link in links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_article, meta={'category': response.meta['category']})


    def parse_article(self, response):
        url = response.url
        category = response.meta['category']
        title = response.xpath(self.title_xpath).get()
        descriptions = response.xpath(self.description_xpath).getall()
        desc = ''.join(descriptions)
        content = Utils.word_60(desc)
        img_src = response.xpath(self.image_xpath).get()
        date = response.xpath(self.date_xpath).get()
        formattedDate = Utils.corporate_nepal_conversion(date)
        news = {
            'title':title.strip(),
            'content_description':content,
            'published_date':formattedDate,
            'image_url':img_src,
            'url':url,
            'category_name':category,
            'is_recent':True,
            'source_name':'corporatenepal'
            }
        PostNews.postnews(news)