import scrapy
from Utils import Utils
from Utils import PostNews
from Utils.Constants import  Standard_Category

class KathmanduPost_Scrapper(scrapy.Spider):
    name = "KathmanduPost"

    def __init__(self, name: str | None = None, **kwargs: any):
        super().__init__(name, **kwargs)

        self.start_url = 'https://kathmandupost.com'
        self.title_xpath = '//h1[@style]/text()'
        self.date_xpath = '//div[@class="updated-time"]/text()'
        self.img_src_xpath = '//div[contains(@class,"row")]/div/img/@data-src'
        self.description_xpath = '//section/p/text()'
        self.categories_xpath = '//ul[@class="list-inline"][@style="display:inline-block;"]/li'
        self.articles_xpath = '//article[@class="article-image "]'
        self.article_link_xpath='.//a/@href'
        self.link_xpath = './/a'

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse)
   
    def parse(self, response):
        categories = response.xpath(self.categories_xpath)
        for category in categories:
            category_link = category.xpath('.//a/@href').get()
            category_text = category.xpath('.//a/text()').get()
            link = response.urljoin(category_link)
            yield scrapy.Request(url=link,callback=self.find_article_links,meta={'category': category_text})


    def find_article_links(self, response):
        articles = response.xpath(self.articles_xpath)[:5]
        for article in articles:
            article_link = article.xpath(self.article_link_xpath).get()
            link = response.urljoin(article_link)
            yield scrapy.Request(url = link,callback = self.parse_article,meta = {'category': response.meta['category']})

    def parse_article(self, response):
        url = response.url
        title = response.xpath(self.title_xpath).get().strip()
        article_date = response.xpath(self.date_xpath).get()
        publishedDate = Utils.kathmandupost_conversion(article_date)
        desc = response.xpath(self.description_xpath).getall()
        content = ''.join(desc)
        description = Utils.word_60(content)
        img_src = response.xpath(self.img_src_xpath).get()
    
        # category_mapping = {
        #     'National': Standard_Category.OTHERS,
        #     'Valley': Standard_Category.OTHERS,
        #     'Money': Standard_Category.FINANCE,
        #     'Culture & Lifestyle': Standard_Category.LIFESTYLE,
        #     'Politics':Standard_Category.POLITICS,
        # }
        category_name = Standard_Category.OTHERS if getattr(Standard_Category, response.meta['category'], None) is None else response.meta['category']


        # category = category_mapping.get(category, category)

        article_data = {
            'category_name': category_name,
            'title': title,
            'published_date': publishedDate,
            'content_description': description,
            'img_url': img_src,
            'url': url,
            'is_recent':True,
            'source_name':'KathmanduPost'
        }
        print(f"---------------category_name: {category_name},---------------------")
        PostNews.postnews(article_data)
