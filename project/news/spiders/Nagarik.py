import scrapy
from time import sleep
import random

class NagarikScraper(scrapy.Spider):
    name="NagarikCategory"

    def __init__(self):
        self.scraped_items = []
        self.article_xpath1='//div[@class="cat-top-part"]/div[@class="row topview"]/div'
        self.article_xpath2='//div[@class="articles"]/article'
        self.link_xpath='.//div[@class="text"]/h1/a'
        self.title_xpath='.//div[@class="text"]/h1/a/text()'
        self.date_xpath='//div[@class="byline mb-5"]/time/text()'
        self.desc_xpath='//article/p/text()'
        self.img_xpath='//div[@class="image mt-2 mx-3"]/img[@class="w-100"]'

    def start_requests(self):
        self.Categories = [
            "व्यापार",
            "खेल",
            "जीवनशैली",
            "मनोरञ्जन",
            "विज्ञान र प्रविधि",
            "राजनीति",
            "अन्तराष्ट्रिय",
            "विश्व",
            "यात्रा",
            "फेसन",
            "शिक्षा",
            "वित्त",
            "कला",
            "अर्थतन्त्र",
            "प्रतिक्रिया",
            "विचार",
            "समाज",
            "स्वास्थ्य",
            "मौसम",
            "अन्य"]

        self.urls = {'नागरिक खोज': 'https://nagariknews.nagariknetwork.com/nagarik-khoj',
                     'राजनीति': 'https://nagariknews.nagariknetwork.com/politics',
                     'घुमफिर':'https://nagariknews.nagariknetwork.com/tag/ghumfir',
                     'समाज': 'https://nagariknews.nagariknetwork.com/social-affairs',
                     'अर्थ': 'https://nagariknews.nagariknetwork.com/economy',
                     'कला': 'https://nagariknews.nagariknetwork.com/arts',
                     'खेल': 'https://nagariknews.nagariknetwork.com/sports',
                     'विचार': 'https://nagariknews.nagariknetwork.com/opinion',
                     'अन्तर्वार्ता': 'https://nagariknews.nagariknetwork.com/interview',
                     'फोटो फिचर': 'https://nagariknews.nagariknetwork.com/photo-feature',
                     'कार्टुन': 'https://nagariknews.nagariknetwork.com/cartoon',
                     'अन्तर्राष्ट्रिय': 'https://nagariknews.nagariknetwork.com/international',
                     'ब्लग':'https://nagariknews.nagariknetwork.com/blog',
                     'स्वास्थ्य':'https://nagariknews.nagariknetwork.com/health',
                     'प्रविधि':'https://nagariknews.nagariknetwork.com/technology',
                     'शिक्षा':'https://nagariknews.nagariknetwork.com/education',
                     'प्रवास':'https://nagariknews.nagariknetwork.com/diaspora',
                    'अन्य':'https://nagariknews.nagariknetwork.com/others',
                    }

        for category, url in self.urls.items():
            try:
                print(f"Searching for articles in {category} from {url}")
                category = category if category in self.Categories else 'अन्य'
                yield scrapy.Request(url=url, callback=self.parse, meta={'url': url, 'category': category})
                t=random.randint(1, 5)
                sleep(t)
            except Exception as e:
                print(f"Error:{e}")
                continue

    def parse(self, response):
        articles=response.xpath(self.article_xpath1)
        if len(articles)!=0:
            for article in articles:
                title=article.xpath(self.title_xpath).get()
                get_link=article.xpath(self.link_xpath).attrib['href']
                link=f"https://nagariknews.nagariknetwork.com{get_link}"
                yield scrapy.Request(url=link, callback=self.parse_article,meta={'title':title,'link':link,'category':response.meta["category"]})
        else:
            length=0
            for article in response.xpath(self.article_xpath2):
                title=article.xpath(self.title_xpath).get().strip()
                get_link=article.xpath(self.link_xpath).attrib['href']
                link=f"https://nagariknews.nagariknetwork.com{get_link}"
                yield scrapy.Request(url=link, callback=self.parse_article,meta={'title':title,'link':link,'category':response.meta["category"]})
                length+=1
                if length==5:
                    break

    def parse_article(self, response):
        title=response.meta['title']
        link=response.meta['link']
        all = response.xpath(self.desc_xpath).getall()
        # description = ' '.join(response.xpath('//article/p/text()').getall()).replace('\t', '')
        description = ''
        for i in all:
            description += i.strip()
        
        img_src=response.xpath(self.img_xpath).attrib['src']
        date=response.xpath(self.date_xpath).get()

        news = {'title':title,'content_description':description,'published_date':date,'img_url':img_src,'url':link,'newspaper':'Nagarik','category_name':response.meta["category"] }
        self.scraped_items.append(news)
        return news
    
    def closed(self,response):
        print("Items after crawling:")
        for item in self.scraped_items:
            print(item)



