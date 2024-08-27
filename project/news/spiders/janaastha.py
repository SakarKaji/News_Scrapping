import scrapy
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews

class janaastha_scrapper(scrapy.Spider):
    name = "janaastha"

    def __init__(self):
        self.articleslink_xpath = '//div[@class="card__details"]//a/@href'
        self.description_xpath = '//div[@class="para__text"]/p/text()'
        self.title_xpath_pre = '//h1[@class="desc__title"]/span/text()'
        self.title_xpath_post = '//h1[@class="desc__title"]/text()[2]'
        self.image_xpath = '//div[@class="news__details-left-desc"]/img/@src'
        self.date_xpath = '//div[@class="date__time"]/p/span/text()'
        self.categories = {
            Standard_Category.TRAVEL: r'https://www.janaaastha.com/category/tourism',
            Standard_Category.ECONOMY: r'https://www.janaaastha.com/category/finance',
            Standard_Category.POLITICS: r'https://www.janaaastha.com/category/politics',
            Standard_Category.SPORTS: r'https://www.janaaastha.com/category/sports',
            Standard_Category.HEALTH: r'https://www.janaaastha.com/category/health',
            Standard_Category.OPINION: r'https://www.janaaastha.com/category/interviews',
            Standard_Category.INTERNATIONAL: r'https://www.janaaastha.com/category/world',
            Standard_Category.ART: r'https://www.janaaastha.com/category/literature',
            Standard_Category.OTHERS: r'https://www.janaaastha.com/category/variety',
            Standard_Category.OTHERS: r'https://www.janaaastha.com/category/inside-city',
            Standard_Category.ART: r'https://www.janaaastha.com/category/litarature-1',
            Standard_Category.OTHERS: r'https://www.janaaastha.com/category/migration',
            Standard_Category.OTHERS: r'https://www.janaaastha.com/category/accident',
            Standard_Category.OTHERS: r'https://www.janaaastha.com/category/crime',
            Standard_Category.OTHERS: r'https://www.janaaastha.com/category/photo-feature',
            Standard_Category.OTHERS: r'https://www.janaaastha.com/category/note-of-descents',
            Standard_Category.ENTERTAINMENT: r'https://www.janaaastha.com/category/entertainment'
        }
        

    def start_requests(self):
        print("---------Scraping janaastha-----------")
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
        titlepre = response.xpath(self.title_xpath_pre).get()
        titlepost = response.xpath(self.title_xpath_post).get()
        title = titlepre +" "+titlepost

        descriptions = response.xpath(self.description_xpath).getall()
        desc = ''.join(descriptions)
        content = Utils.word_60(desc)
        img_src = response.xpath(self.image_xpath).get()
        date = response.xpath(self.date_xpath).get()
        formattedDate = Utils.janaastha_conversion(date)
        news = {
            'title':title.strip(),
            'content_description':content,
            'published_date':formattedDate,
            'image_url':img_src,
            'url':url,
            'category_name':category,
            'is_recent':True,
            'source_name':'janaastha'
            }
        PostNews.postnews(news)