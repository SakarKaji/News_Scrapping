
import scrapy
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews


class arthikabiyan_scrapper(scrapy.Spider):
    name = "arthikabiyan"

    def __init__(self):
        self.articleslink_xpath = '//div[@class="flex relative flex-col justify-between w-full overflow-hidden min-w-[12rem]"]/a/@href'
        self.description_xpath = '//div[@id="article_html_content"]//p/text()'
        self.title_xpath = '//div[@class="flex w-full  flex-col  md:flex-row  gap-5 p-3 md:p-9 "]//span[@class=" text-2xl  md:text-4xl font-bold leading-relaxed "]//text()'
        self.image_xpath = '//div[@class=" relative w-[7/10] h-[calc(7/10 * 1.68/1)]  "]/img/@src'
        self.date_xpath = '//span[contains(@class, "anticon anticon-clock-circle")]/following-sibling::span[1]/text()'
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
        unwanted_chars = ['\xa0', '\x00', '\n', '\u202f', '\u200d']
        for char in unwanted_chars:
            content = content.replace(char, '')
        news = {
            'title': title.strip(),
            'content_description': content,
            'published_date': formattedDate,
            'url': url,
            'category': category,
            'is_recent': True,
            'source': 'abhiyandaily'
        }
        if img_src:
            news['image_url'] = img_src
        print(news)
        PostNews.postnews(news)
