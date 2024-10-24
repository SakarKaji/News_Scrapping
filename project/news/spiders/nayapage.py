import scrapy
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews

class nayapage_scrapper(scrapy.Spider):
    name = "nayapage"

    def __init__(self):
        self.articleslink_xpath_business = '//div[contains(@class,"uk-grid")]/div[contains(@class,"last-border")]/a/@href'
        self.articleslink_xpath_business2 = '//div[contains(@class,"uk-grid-margin uk-first-column")]//div[contains(@class,"last-border")]/a/@href'
        self.articleslink_xpath_others = '//div[contains(@class,"uk-card uk-card-default uk-card-body uk-margin-bottom uk-card-small")]/div/h3/a/@href'
        self.articleslink_xpath_entertainment= '//div[contains(@class,"uk-card uk-card-hover uk-card-default uk-margin")]/a/@href'
        self.description_xpath = '//article/p/text()'
        self.title_xpath = '//article/header/h1/text()'
        self.image_xpath = '//article/figure/img/@data-src'
        self.date_xpath = '//div[@class="uk-comment-meta uk-margin-remove-top uk-text-meta"]/text()'
        self.categories = {
            Standard_Category.HEALTH: r'https://www.nayapage.com/archives/category/%e0%a4%b8%e0%a5%8d%e0%a4%b5%e0%a4%be%e0%a4%b8%e0%a5%8d%e0%a4%a5%e0%a5%8d%e0%a4%af-%e0%a4%9c%e0%a5%80%e0%a4%b5%e0%a4%a8%e0%a4%b6%e0%a5%88%e0%a4%b2%e0%a5%80',
            Standard_Category.INTERNATIONAL: r'https://www.nayapage.com/archives/category/%e0%a4%97%e0%a5%8d%e0%a4%b2%e0%a5%8b%e0%a4%ac%e0%a4%b2',
            Standard_Category.ENTERTAINMENT: r'https://www.nayapage.com/archives/category/%e0%a4%ae%e0%a4%a8%e0%a5%8b%e0%a4%b0%e0%a4%a8%e0%a5%8d%e0%a4%9c%e0%a4%a8',
            Standard_Category.BUSINESS: r'https://www.nayapage.com/archives/category/%e0%a4%b5%e0%a4%bf%e0%a4%9c%e0%a4%a8%e0%a5%87%e0%a4%b8',
            Standard_Category.SPORTS: r'https://www.nayapage.com/archives/category/%e0%a4%96%e0%a5%87%e0%a4%b2%e0%a4%95%e0%a5%81%e0%a4%a6',
            Standard_Category.OPINION: r'https://www.nayapage.com/archives/category/%e0%a4%93%e0%a4%aa%e0%a5%87%e0%a4%a1/%e0%a4%b5%e0%a4%bf%e0%a4%9a%e0%a4%be%e0%a4%b0',
            Standard_Category.ART: r'https://www.nayapage.com/archives/category/%e0%a4%b8%e0%a4%be%e0%a4%b9%e0%a4%bf%e0%a4%a4%e0%a5%8d%e0%a4%af',
            Standard_Category.SCIENCE_AND_TECHNOLOGY: r'https://www.nayapage.com/archives/category/%e0%a4%b5%e0%a4%bf%e0%a4%9c%e0%a5%8d%e0%a4%9e%e0%a4%be%e0%a4%a8-%e0%a4%b0-%e0%a4%aa%e0%a5%8d%e0%a4%b0%e0%a4%b5%e0%a4%bf%e0%a4%a7%e0%a4%bf',
            Standard_Category.OTHERS: r'https://www.nayapage.com/archives/category/%e0%a4%85%e0%a4%aa%e0%a4%b0%e0%a4%be%e0%a4%a7-%e0%a4%b8%e0%a5%81%e0%a4%b0%e0%a4%95%e0%a5%8d%e0%a4%b7%e0%a4%be',
            Standard_Category.OTHERS: r'https://www.nayapage.com/archives/category/%e0%a4%b8%e0%a4%ae%e0%a4%be%e0%a4%9a%e0%a4%be%e0%a4%b0'

        }
        

    def start_requests(self):
        for category in self.categories:
            try:
                yield scrapy.Request(url=self.categories[category], callback=self.parse, meta={'category': category})
            except Exception as e:
                print(f"Error:{e}")
                continue

    def parse(self, response):
        if(response.meta['category'] == 'business'):
            link1= response.xpath(self.articleslink_xpath_business).getall()
            link2 = response.xpath(self.articleslink_xpath_business2).getall()
            links = link1 + link2
        elif(response.meta['category'] == 'entertainment'):
            links = response.xpath(self.articleslink_xpath_entertainment).getall()
        else:
            links = response.xpath(self.articleslink_xpath_others).getall()
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
        formattedDate = Utils.nayapage_datetime(date)

        news = {
            'title':title.strip(),
            'content_description':content,
            'published_date':formattedDate,
            'image_url':img_src,
            'url':url,
            'category_name':category,
            'is_recent':True,
            'source_name':'nayapage'
            }
        print(news)
        PostNews.postnews(news)