import os
import random

from celery.app import shared_task
from celery.app.base import Celery
from scrapy.crawler import CrawlerProcess
from scrapy import settings
# from scrapy import log, project, signals
from twisted.internet import reactor
from billiard import Process
from scrapy.utils.project import get_project_settings
from news.spiders import (
    EverestHeadlines, saralpatrika, Annapurna, Myrepublica,
    eKantipur, Nagarik, kathmanduPost, Ratopati, RatopatiEnglish,
    rajdhani, reportersnepal, Onlinekhabar, gorkhapatra, techlekh,
    arthasarokar, arthikabiyan, aajakokhabar, himalkhabar, nayapage,
    lokantar, corporatenepal, eadarshsamaj, janaastha, khabarhub,
    bizmandu, baarakhari, setopati, bbcNepali, news24, onlinekhabarEnglish,
    onlinemajdur, thakhabar, merolagani, ictsamachar, timesofindia
)
from celery import Celery
from celery.schedules import crontab

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from Utils import Email
from Utils import Utils

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Celery application setup
app = Celery('tasks', broker=os.environ.get("NEWS_REDIS_URL"))
app.config_from_object('celeryconfig')

# Cron interval from environment
CRON_INTERVAL = os.environ.get("CRON_JOB_INTERVAL")

try:
    CRON_INTERVAL = int(CRON_INTERVAL)  # Convert to integer
except ValueError:
    raise ValueError("CRON_JOB_INTERVAL must be a valid integer.")


# Celery beat schedule for periodic task
app.conf.beat_schedule = {
    "task-run_scraper": {
        "task": "run_scraper",
        "schedule": crontab(minute=f"*/{CRON_INTERVAL}"),
    },
}

# app.conf.beat_schedule = {
#     "task-run_scraper": {
#         "task": "run_scraper",
#         "schedule": crontab(minute="*/1"),  # Runs every 1 minutes
#     },
# }

spiders = [
    eKantipur.EKantipur_Scrapper,
    kathmanduPost.KathmanduPost_Scrapper,
    EverestHeadlines.EverestHeadlineScrapper,
    Ratopati.Ratopati_scrapper,
    Onlinekhabar.OnlineKhabarScrapper,
    gorkhapatra.GorkhaPatraOnlineScrapper,
    RatopatiEnglish.EnglishRatopatiScrapper,
    techlekh.techlekh_scrapper,
    himalkhabar.himalkhabar_scrapper,
    lokantar.lokantar_scrapper,
    eadarshsamaj.eadarsha_scrapper,
    janaastha.janaastha_scrapper,
    khabarhub.khabarhub_scrapper,
    aajakokhabar.aajakokhabar_scrapper,
    arthikabiyan.arthikabiyan_scrapper,
    bizmandu.bizamandu_scrapper,
    setopati.Setopati_Scrapper,
    bbcNepali.bbcNepali_scrapper,
    onlinekhabarEnglish.OnlinekhabarEnglish_scrapper,
    onlinemajdur.Onlinemajdur_scrapper,
    thakhabar.Thakhabar_scrapper,
    rajdhani.rajdhanidaily_scrapper,
    merolagani.Merolagani_scrapper,
    ictsamachar.ictsamachar_scrapper,
    timesofindia.TimesOfIndia_Scrapper,
]
# Myrepublica.Myrepublica_Scrapper,
# Nagarik.NagarikScraper,
# Annapurna.AnnapurnaScraper, ## rss feed
# news24.News24Scrapper,  #someproblem
# setopatiEnglish.setopatiEnglish
# hamrokhelkud.hamrokhelkud_scrapper,
# HimalayanTimes.HimalayanScraper, ip blocked
# saralpatrika.saralpatrika_scrapper,   #saral patrika chalena
# arthasarokar.arthasarokar_scrapper, #date issue
# corporatenepal.corporatenepal_scrapper,  # not working
# reportersnepal.reportersnepal_scrapper, # chaleko chhaina
# nayapage.nayapage_scrapper,
# baarakhari.baarakhari_scrapper,


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


def run_spider(url=""):
    random.shuffle(spiders)
    for spider in spiders:
        # spider = test2.MySpider
        crawler = UrlCrawlerScript(spider)
        crawler.start()
        crawler.join()
    # sent = Email.Report_Email()

    # if sent:
    #     Utils.delete_report_file()


@app.task(name='run_scraper')
def crawl():
    return run_spider()
