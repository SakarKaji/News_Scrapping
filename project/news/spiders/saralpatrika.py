import scrapy
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews

class saralpatrika_scrapper(scrapy.Spider):
    name = "saralpatrika"

    def __init__(self):
        self.articleslink_xpath = '//div[@class="overlay--news"]/a/@href'
        self.description_xpath = '//div[@class="content-area"]/p/text()'
        self.title_xpath = '//h2[@class="breaking__news--title"]/text()'
        self.image_xpath = '//div[@class="featured-img"]/img/@src'
        self.date_xpath = '//span[@class="post-hour"]/text()'
        self.categories = {
            Standard_Category.POLITICS: r'https://www.saralpatrika.com/category/politics/',
            Standard_Category.ECONOMY: r'https://www.saralpatrika.com/category/saral-artha/',
            Standard_Category.OPINION: r'https://www.saralpatrika.com/category/bichar/',
            Standard_Category.SPORTS: r'https://www.saralpatrika.com/category/sports/',
            Standard_Category.TRAVEL: r'https://www.saralpatrika.com/category/tourism/',
            Standard_Category.ENTERTAINMENT: r'https://www.saralpatrika.com/category/entertainment/',
            Standard_Category.INTERNATIONAL: r'https://www.saralpatrika.com/category/world/',
            Standard_Category.SOCIETY: r'https://www.saralpatrika.com/category/samaj/',
            Standard_Category.SCIENCE_AND_TECHNOLOGY: r'https://www.saralpatrika.com/category/science-tech/',
            Standard_Category.ART: r'https://www.saralpatrika.com/category/kala-sahitya/',

            Standard_Category.OTHERS: r'https://www.saralpatrika.com/category/spiritual/',
            Standard_Category.OTHERS: r'https://www.saralpatrika.com/category/interesting/',
            Standard_Category.OTHERS: r'https://www.saralpatrika.com/category/sarcasm/',
            Standard_Category.OTHERS: r'https://www.saralpatrika.com/category/photo-feature/',
            
        }
        

    def start_requests(self):
        print("---------Scraping saralpatrika----------")
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
        print(category)
        title = response.xpath(self.title_xpath).get()

        descriptions = response.xpath(self.description_xpath).getall()
        desc = ''.join(descriptions)
        content = Utils.word_60(desc)
        img_src = response.xpath(self.image_xpath).get()
        date = response.xpath(self.date_xpath).get()
        print(date)
        formattedDate = Utils.Saralpatrika_conversion(date)
        print(formattedDate)

        news = {
            'title':title.strip(),
            'content_description':content,
            'published_date':formattedDate,
            'image_url':img_src,
            'url':url,
            'category_name':category,
            'is_recent':True,
            'source_name':'saralpatrika'
            }
        PostNews.postnews(news)