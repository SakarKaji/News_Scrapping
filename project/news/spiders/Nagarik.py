import scrapy
from Utils.Constants import Standard_Category
from Utils import Utils
from Utils import PostNews


class NagarikScraper(scrapy.Spider):
    name = "NagarikCategory"

    def __init__(self):
        self.scraped_items = []
        self.article_xpath1 = '//div[@class="cat-top-part"]/div[@class="row topview"]/div'
        self.article_xpath2 = '//div[@class="articles"]/article'
        self.link_xpath = './/div[@class="text"]/h1/a'
        self.title_xpath = './/div[@class="text"]/h1/a/text()'
        self.date_xpath = '//div[@class="byline mb-5"]/time/text()'
        self.desc_xpath = '//article/p/text()'
        self.img_xpath = '//div[@class="image mt-2 mx-3"]/img[@class="w-100"]'

        self.categories = {
            Standard_Category.POLITICS: r'https://nagariknews.nagariknetwork.com/politics',
            Standard_Category.SOCIETY: r'https://nagariknews.nagariknetwork.com/social-affairs',
            Standard_Category.ECONOMY: r'https://nagariknews.nagariknetwork.com/economy',
            Standard_Category.OPINION: r'https://nagariknews.nagariknetwork.com/opinion',
            Standard_Category.TRAVEL: r'https://nagariknews.nagariknetwork.com/tag/ghumfir',
            Standard_Category.SPORTS: r'https://nagariknews.nagariknetwork.com/sports',
            Standard_Category.EDUCATION: r'https://nagariknews.nagariknetwork.com/education',
            Standard_Category.SCIENCE_AND_TECHNOLOGY: r'https://nagariknews.nagariknetwork.com/technology',
            Standard_Category.INTERNATIONAL: r'https://nagariknews.nagariknetwork.com/international',
            Standard_Category.HEALTH: r'https://nagariknews.nagariknetwork.com/health',
            Standard_Category.OTHERS: r'https://nagariknews.nagariknetwork.com/photo-feature',
            Standard_Category.OTHERS: r'https://nagariknews.nagariknetwork.com/diaspora',
            Standard_Category.OTHERS: r'https://nagariknews.nagariknetwork.com/interview',

        }

    def start_requests(self):
        for category in self.categories:
            try:
                yield scrapy.Request(url=self.categories[category], callback=self.parse, meta={'category': category})
            except Exception as e:
                print(f"Error:{e}")
                continue

    def parse(self, response):
        article1 = response.xpath(self.article_xpath1)
        article2 = response.xpath(self.article_xpath2)
        articles = article1 + article2

        for article in articles:
            title = article.xpath(self.title_xpath).get().strip()
            get_link = article.xpath(self.link_xpath).attrib['href']
            link = f"https://nagariknews.nagariknetwork.com{get_link}"
            yield scrapy.Request(url=link, callback=self.parse_article, meta={'title': title, 'link': link, 'category': response.meta["category"]})

    def parse_article(self, response):
        category = response.meta['category']
        title = response.meta['title']
        link = response.meta['link']
        img_src = response.xpath(self.img_xpath).attrib['src']
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
            'category_name': category,
            'is_recent': True,
            'source_name': 'nagariknews'
        }
        print(
            f"---------------category_name: {category},---------------------")
        PostNews.postnews(news)
