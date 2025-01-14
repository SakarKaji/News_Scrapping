import scrapy
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews
from datetime import datetime


class NagarikScraper(scrapy.Spider):
    name = "NagarikCategory"

    def __init__(self):
        self.scraped_items = []
        self.article_xpath1 = '//div[@class="cat-top-part"]/div[@class="row topview"]/div'
        self.article_xpath2 = '//div[@class="articles"]/article'
        self.link_xpath = './/div[@class="text"]/h1/a'
        self.title_xpath = '(//div[@class="container"]/div[contains(@class,"row")]/div[contains(@class,"col")]/h1)[1]/text()'
        self.date_xpath = '//div[@class="byline mb-5"]/time/text()'
        self.desc_xpath = '//article/p/text()'
        self.img_xpath = '(//div[contains(@class,"image")]/img)[1]'
        self.img_xpath2 = '(//div[contains(@class,"figure")]/img)[1]'
        self.outer_date_xpath = "//time[contains(@class,'npdate')]/@data-pdate"
        self.dates = []
        self.links = []
        self.today_date = datetime.today().strftime('%Y-%m-%d')

        self.categories = {
            Standard_Category.POLITICS: r'https://nagariknews.nagariknetwork.com/politics',
            Standard_Category.SOCIETY: r'https://nagariknews.nagariknetwork.com/social-affairs',
            Standard_Category.ECONOMY: r'https://nagariknews.nagariknetwork.com/economy',
            Standard_Category.ART: r'https://nagariknews.nagariknetwork.com/arts',
            Standard_Category.OPINION: r'https://nagariknews.nagariknetwork.com/opinion',
            Standard_Category.TRAVEL: r'https://nagariknews.nagariknetwork.com/tag/ghumfir',
            Standard_Category.SPORTS: r'https://nagariknews.nagariknetwork.com/sports',
            Standard_Category.EDUCATION: r'https://nagariknews.nagariknetwork.com/education',
            Standard_Category.SCIENCE_AND_TECHNOLOGY: r'https://nagariknews.nagariknetwork.com/technology',
            Standard_Category.INTERNATIONAL: r'https://nagariknews.nagariknetwork.com/international',
            Standard_Category.HEALTH: r'https://nagariknews.nagariknetwork.com/health',
            Standard_Category.OTHERS: [
                r'https://nagariknews.nagariknetwork.com/tag/biwidh',
                r'https://nagariknews.nagariknetwork.com/others',
                r'https://nagariknews.nagariknetwork.com/blog',
                r'https://nagariknews.nagariknetwork.com/nagarik-khoj',
                r'https://nagariknews.nagariknetwork.com/interview',
                r'https://nagariknews.nagariknetwork.com/diaspora',
                r'https://nagariknews.nagariknetwork.com/photo-feature',
                r'https://nagariknews.nagariknetwork.com/interview',
            ]
        }

    def start_requests(self):
        for category in self.categories:
            try:
                if category == "others":
                    for inner_category_url in self.categories[category]:
                        print(f"Link :: {inner_category_url}")
                        yield scrapy.Request(url=inner_category_url, callback=self.parse, meta={'category': category})
                else:
                    yield scrapy.Request(url=self.categories[category], callback=self.parse, meta={'category': category})

            except Exception as e:
                print(f"Error: {e}")

    def parse(self, response):
        article1 = response.xpath(self.article_xpath1)
        article2 = response.xpath(self.article_xpath2)
        articles = article1 + article2

        outer_dates = response.xpath(self.outer_date_xpath)
        for date in outer_dates:
            date_obj = datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S")
            date = date_obj.strftime("%Y-%m-%d")
            self.dates.append(date)

        for article in articles:
            get_link = article.xpath(self.link_xpath).attrib['href']
            print(f"Linker:: {get_link}")
            link = f"https://nagariknews.nagariknetwork.com{get_link}"
            self.links.append(link)

        for link, date in zip(self.links, self.dates):
            if date != self.today_date:
                break
            yield scrapy.Request(url=link, callback=self.parse_article, meta={'link': link, 'category': response.meta["category"]})

    def parse_article(self, response):
        category = response.meta['category']
        title = response.xpath(self.title_xpath).get().strip()
        link = response.meta['link']

        try:
            img_src = response.xpath(self.img_xpath).attrib['src']
        except:
            img_src = response.xpath(self.img_xpath2).attrib['src']

        all = response.xpath(self.desc_xpath).getall()
        desc = ''.join(all)
        description = Utils.word_60(desc)
        date = response.xpath(self.date_xpath).get()
        formatteddate = Utils.nagariknews__dateconverter(date)

        news = {
            'title': title,
            'content_description': description,
            'published_date': formatteddate,
            'img_url': img_src,
            'url': link,
            'category': category,
            'is_recent': True,
            'source': 'nagariknews'
        }
        PostNews.postnews(news)
