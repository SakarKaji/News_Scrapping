# http://stackoverflow.com/questions/24232744/scrapy-spider-not-following-links-when-using-celery

from celery.app import shared_task
from celery.app.base import Celery
from scrapy.crawler import CrawlerProcess
from scrapy import settings
# from scrapy import log, project, signals
from twisted.internet import reactor
from billiard import Process
from scrapy.utils.project import get_project_settings
from news.spiders import Annapurna,gorkhapatra,Nagarik, Myrepublica, eKantipur, kathmanduPost, EverestHeadlines,Ratopati,Onlinekhabar,RatopatiEnglish
from celery import Celery
from celery.schedules import crontab

app = Celery('tasks', broker='redis://localhost:6379')
app.config_from_object('celeryconfig')

app.conf.beat_schedule = {
    "task-news_scrapper-1": {
        "task": "news_scrapper-1",
        "schedule": crontab(minute="*"),
    },
}

spiders = [
         Annapurna.AnnapurnaScraper,
         Myrepublica.Myrepublica_Scrapper,
         eKantipur.EKantipur_Scrapper,
         Nagarik.NagarikScraper,
         kathmanduPost.KathmanduPost_Scrapper,
         EverestHeadlines.EverestHeadlineScrapper,
         Ratopati.Ratopati_scrapper,
         Onlinekhabar.OnlineKhabarScrapper,
         gorkhapatra.GorkhaPatraOnlineScrapper,
         RatopatiEnglish.EnglishRatopatiScrapper
        ]
        # HimalayanTimes.HimalayanScraper, ip blocked 

class UrlCrawlerScript(Process):
        def __init__(self, spider):
            Process.__init__(self)
            settings = get_project_settings()
            self.crawler = CrawlerProcess(settings)
            # self.crawler.configure()
            # self.crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
            self.spider = spider

        def run(self):
            self.crawler.crawl(self.spider)
            self.crawler.start()
            # reactor.run()

def run_spider(url = ""):
    for spider in spiders:
        # spider = test2.MySpider
        crawler = UrlCrawlerScript(spider)
        crawler.start()
        crawler.join()

@app.task(name='news_scrapper-1')
def crawl():
    return run_spider()