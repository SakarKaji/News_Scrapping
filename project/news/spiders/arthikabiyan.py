
import scrapy
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews

class arthikabiyan_scrapper(scrapy.Spider):
    name = "arthikabiyan"

    def __init__(self):
        self.articleslink_xpath = '//div[@class="flex relative flex-col justify-between w-full overflow-hidden min-w-[12rem]"]/a/@href'
        self.description_xpath = '//div[@class=" text-xl  md:text-xl  leading-loose md:leading-8"]/p/text()'
        self.title_xpath = '//span[@class=" text-4xl font-bold  leading-10 "]/text()'
        self.image_xpath = '//div[@class=" relative w-[7/10] h-[calc(7/10 * 1.68/1)]  "]/img/@src'
        self.date_xpath = '//div[@class="flex items-start gap-2 text-gray-400 "]/span/text()[2]'
        self.categories = {
            Standard_Category.OPINION: r'https://www.abhiyandaily.com/category/lekh-drssttikonn',
            Standard_Category.ECONOMY: r'https://www.abhiyandaily.com/category/lgaanii',
            Standard_Category.ECONOMY: r'https://www.abhiyandaily.com/category/smaacaar',
            Standard_Category.ECONOMY: r'https://www.abhiyandaily.com/category/baingking-gtividhi',
            Standard_Category.INTERNATIONAL: r'https://www.abhiyandaily.com/category/antrraassttriy',
            Standard_Category.OTHERS: r'https://www.abhiyandaily.com/category/abhiyaan-prishisstt-splimentt',
            Standard_Category.OTHERS: r'https://www.abhiyandaily.com/category/vividh'
        }
        

    def start_requests(self):
        print("---------Scraping Arthik Abiyan-----------")
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
        formattedDate = Utils.arthiknews_date_conversion(date)

        news = {
            'title':title.strip(),
            'content_description':content,
            'published_date':formattedDate,
            'image_url':img_src,
            'url':url,
            'category_name':category,
            'is_recent':True,
            'source_name':'abhiyandaily'
            }
        PostNews.postnews(news)