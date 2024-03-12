import scrapy
from Utils import Utils
from Utils import PostNews
from Utils.Constants import Standard_Category

class Myrepublica_Scrapper(scrapy.Spider):
    name = 'Myrepublica'

    def __init__(self, name: str | None = None, **kwargs: any):
        super().__init__(name, **kwargs)

        self.start_urls = ['https://myrepublica.nagariknetwork.com/']
        self.data = []
        self.navpath = '//ul[@class="nav navbar-nav"]/li'
        self.titlePath = '//div[@class="main-heading"]/h2/text()'
        self.imagepath = '//div[@class="inner-featured-image"]/img/@src'
        self.alt_imagepath = '//figure[@class="article__header__img"]/img/@src' 
        self.contentpath= '//div[@id="newsContent"]/p/text()'
        self.datepath = '//*[@id="main-hightlight-categories-news"]/div/div/div/div[1]/div[1]/div[1]/div[1]/div/p/text()[2]'

    def start_request(self):
        yield scrapy.Request(url= self.start_urls, callback=self.parse)

    def parse(self, response):
        for links in response.xpath(self.navpath):
            href = links.css('a').attrib["href"]
            category = links.xpath('.//a/span/text()').get()
            link = 'https://myrepublica.nagariknetwork.com' + href
            if link and category != None:
                yield scrapy.Request(url=link, callback=self.parse_link, meta={'link': link, 'category':category})

    def parse_link(self, response):
        if (response.meta['category'] == "OPINION"):
            for div in response.xpath('//div[contains(@class,"first-on first-list")]/h3'): #have different  xpath for container
                href = div.css('a').attrib["href"]
                Link = 'https://myrepublica.nagariknetwork.com' + href
                linkdict = {'category':response.meta['category'], 'link':Link}
                self.data.append(linkdict)
        else:
            for div in response.xpath('//div[contains(@class ,"main-heading")]'):
                href = div.css('a').attrib["href"]
                Link = 'https://myrepublica.nagariknetwork.com' + href
                linkdict = {'category':response.meta['category'], 'link':Link}
                self.data.append(linkdict)
        for url in self.data:
            yield scrapy.Request(url=url['link'], callback=self.parse_article,meta={'link': url['link'], 'category':url['category']})

    def parse_article(self,response):
        image= response.xpath(self.imagepath).get()
        if( image == None):
            image = response.xpath(self.alt_imagepath).get() 
        title = (response.xpath(self.titlePath).get()).strip()
        contentList = response.xpath(self.contentpath).getall()
        content = ''.join(contentList)
        description = Utils.word_60(content)

        date = response.xpath(self.datepath).get()
        if(date == None):
            date = response.xpath('//div[@class="headline-time pull-left"]/p/text()[2]').get()
        elif(date == None):
            date = response.xpath('//div[@class="article__header"]/span/text()[2]').get()

        category_name = 'Others' if getattr(Standard_Category, response.meta['category'], None) is None else response.meta['category']

        publishdate = Utils.republica_conversion(date)
       
        news= {     "title": title,
                    "content_description" : description,
                    "image_url" : image,
                    "url": response.meta['link'],
                    "category_name": category_name,
                    "published_date" : publishdate,
                    'is_recent':True,
                  'source_name':'myrepublica'
                }
        PostNews.postnews(news)
        print(f"---------------category_name: {category_name},---------------------")


 

