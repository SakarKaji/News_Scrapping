import scrapy
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews

class eadarsha_scrapper(scrapy.Spider):
    name = "eadarsha"

    def __init__(self):
        self.articleslink_xpath = '//h4[@class="card-text mb-1"]/a/@href'
        self.articleslink_xpath_sports = '//h5[@class="mt-3 text-center"]/a/@href'
        self.description_xpath = '//div[@class="the-content"]/p/text()'
        self.title_xpath = '//h1[@class="post-title mb-2"]/text()'
        self.image_xpath = '//div[@class="wp-caption mb-4"]/img/@src'
        self.date_xpath = '//span[@class="ss-author pull-left"]/text()[2]'
        self.categories = {
            Standard_Category.OPINION: r'https://www.eadarsha.com/nep/article/',
            Standard_Category.POLITICS: r'https://www.eadarsha.com/nep/category/news/politics/',
            Standard_Category.SOCIETY: r'https://www.eadarsha.com/nep/category/news/nepal/',
            Standard_Category.INTERNATIONAL: r'https://www.eadarsha.com/nep/category/news/world/',
            Standard_Category.ENTERTAINMENT: r'https://www.eadarsha.com/nep/category/news/glamour/',
            Standard_Category.EDUCATION: r'https://www.eadarsha.com/nep/category/news/education/',
            Standard_Category.BUSINESS: r'https://www.eadarsha.com/nep/category/news/business/',
            Standard_Category.SCIENCE_AND_TECHNOLOGY: r'https://www.eadarsha.com/nep/category/news/science/',
            Standard_Category.SPORTS: r'https://www.eadarsha.com/sports/',
            Standard_Category.TRAVEL: r'https://www.eadarsha.com/nep/category/news/tourism/',
            Standard_Category.ART: r'https://www.eadarsha.com/nep/category/news/arts/',
            Standard_Category.OTHERS: r'https://www.eadarsha.com/nep/editorial/',
            Standard_Category.OTHERS: r'https://www.eadarsha.com/nep/photo_gallery/'
        }
        

    def start_requests(self):
        print("---------Scraping Eadarsh-----------")
        for category in self.categories:
            try:
                yield scrapy.Request(url=self.categories[category], callback=self.parse, meta={'category': category})
            except Exception as e:
                print(f"Error:{e}")
                continue

    def parse(self, response):

        if(response.meta['category']== 'sports'):
            links = response.xpath(self.articleslink_xpath_sports).getall()
        else:
            links = response.xpath(self.articleslink_xpath).getall()


        for link in links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_article, meta={'category': response.meta['category']})


    def parse_article(self, response):
        url = response.url
        category = response.meta['category']
        title = response.xpath(self.title_xpath).extract_first()
        descriptions = response.xpath(self.description_xpath).getall()
        desc = ''.join(descriptions)
        content = Utils.word_60(desc)
        img_src = response.xpath(self.image_xpath).get()
        date = response.xpath(self.date_xpath).get()
        formattedDate = Utils.eAdarsha_conversion(date)

        news = {
            'title':title.strip(),
            'content_description':content,
            'published_date':formattedDate,
            'image_url':img_src,
            'url':url,
            'category_name':category,
            'is_recent':True,
            'source_name':'eadarsha'
            }
        PostNews.postnews(news)