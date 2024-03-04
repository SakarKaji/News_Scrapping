import json
import scrapy

class onlinekhabar(scrapy.Spider):
    name = 'onlinekhabar'

   
    
    def __init__(self, name: str | None = None, **kwargs: any):
        super().__init__(name, **kwargs)
        self.categorylsit = [ 'SPORTS' , 'LIFESTYLE', 'ENTERTAINMENT' ,
        'SCIENCE_AND_TECHNOLOGY' ,
        'POLITICS' ,
        'INTERNATIONAL' ,
        'TRAVEL' ,
        'FASHION' ,
        'EDUCATION' ,
        'FINANCE',
        'ART',
        'ECONOMY' ,
        'OPINION' ,
        'SOCIETY' ,
        'HEALTH' ,
        'WEATHER' 
        ]
        self.start_urls = ['https://myrepublica.nagariknetwork.com/']
        self.data = []
        self.alldata= []
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
        content = ''.join(response.xpath(self.contentpath).getall())
        date = response.xpath(self.datepath).get()
        if(date == None):
            date = response.xpath('//div[@class="headline-time pull-left"]/p/text()[2]').get()
        elif(date == None):
            date = response.xpath('//div[@class="article__header"]/span/text()[2]').get()

        publishdate = ((date.strip()).replace(' By:',''))
        fromattedate = " ".join(publishdate.split(' ')[:3])
        news= {     "title": title,
                    "content_description" : content,
                    "image_url" : image,
                    "url": response.meta['link'],
                    "category_name": 'Others' if response.meta['category'] not in self.categorylsit else response.meta['category'],
                    "published_date" : fromattedate,
                }
        self.alldata.append(news)
        print(json.dumps(self.alldata,indent=4,ensure_ascii=False))

if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'LOG_ENABLED': False,  
        'LOG_STDOUT': False,   
    })
    
  
    process.crawl(onlinekhabar)
    process.start()
 

