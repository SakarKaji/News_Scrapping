import os
import importlib

from celery import Celery, group
from celery.schedules import crontab

from scrapy.crawler import CrawlerProcess
from scrapy import settings
from scrapy.utils.project import get_project_settings

from billiard import Process
from news.spiders import *
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

# Redis broker transport options with timeouts
app.conf.broker_transport_options = {
    # 'visibility_timeout': 3600,       # Task result visibility in seconds
    'socket_timeout': 30,             # Redis socket timeout in seconds
    'socket_connect_timeout': 10,     # Redis connection timeout in seconds
    'retry_on_timeout': True          # Retry if Redis connection times out
}

# Celery task settings
# Acknowledge task only after successful execution
app.conf.task_acks_late = True
# Requeue the task if the worker is lost
app.conf.task_reject_on_worker_lost = True
app.conf.task_soft_time_limit = 30      # Task soft time limit in seconds

# List of spiders to be scraped
spiders = [
    'news.spiders.eKantipur.EKantipur_Scrapper',
    'news.spiders.kathmanduPost.KathmanduPost_Scrapper',
    'news.spiders.EverestHeadlines.EverestHeadlineScrapper',
    'news.spiders.Ratopati.Ratopati_scrapper',
    'news.spiders.Onlinekhabar.OnlineKhabarScrapper',
    'news.spiders.gorkhapatra.GorkhaPatraOnlineScrapper',
    'news.spiders.RatopatiEnglish.EnglishRatopatiScrapper',
    'news.spiders.techlekh.techlekh_scrapper',
    'news.spiders.himalkhabar.himalkhabar_scrapper',
    'news.spiders.eadharshsamaj.eadarsha_scrapper',
    'news.spiders.janaastha.janaastha_scrapper',
    'news.spiders.khabarhub.khabarhub_scrapper',
    'news.spiders.aajakokhabar.aajakokhabar_scrapper',
    'news.spiders.arthikabiyan.arthikabiyan_scrapper',
    'news.spiders.bizmandu.bizamandu_scrapper',
    'news.spiders.setopati.Setopati_Scrapper',
    'news.spiders.bbcNepali.bbcNepali_scrapper',
    'news.spiders.onlinekhabarEnglish.OnlinekhabarEnglish_scrapper',
    'news.spiders.onlinemajdur.Onlinemajdur_scrapper',
    'news.spiders.thakhabar.Thakhabar_scrapper',
    'news.spiders.rajdhani.rajdhanidaily_scrapper',
    'news.spiders.merolagani.Merolagani_scrapper',
    'news.spiders.ictsamachar.ictsamachar_scrapper',
    'news.spiders.RisingNepal.RisingNepal_scrapper',
    'news.spiders.timesofindia.TimesOfIndia_Scrapper',
    'news.spiders.setopatiEnglish.SetopatiEnglish_Scrapper',
    'news.spiders.arthasarokar.arthasarokar_scrapper',
    'news.spiders.lokantar.lokantar_scrapper',
    'news.spiders.Nagarik.NagarikScraper',
]
# Myrepublica.Myrepublica_Scrapper,
# hamrokhelkud.hamrokhelkud_scrapper,  needs bypass - 403 error
# Annapurna.AnnapurnaScraper, ## rss feed
# news24.News24Scrapper,  #someproblem
# HimalayanTimes.HimalayanScraper, ip blocked
# saralpatrika.saralpatrika_scrapper,   #saral patrika chalena
# corporatenepal.corporatenepal_scrapper,  # not working
# reportersnepal.reportersnepal_scrapper, # chaleko chhaina
# nayapage.nayapage_scrapper,
# baarakhari.baarakhari_scrapper,
# nayapage.nayapage_scrapper,


class UrlCrawlerScript(Process):
    def __init__(self, spider):
        super().__init__()
        settings = get_project_settings()
        self.crawler = CrawlerProcess(settings)
        self.spider = spider

    def run(self):
        self.crawler.crawl(self.spider)
        self.crawler.start()


@app.task(name='run_scraper')
def crawl():
    # Create separate tasks for each spider
    spider_tasks = [run_single_spider.s(spider_name)
                    for spider_name in spiders]

    # Group to allow distribution across multiple workers
    job = group(spider_tasks)
    return job.apply_async()


@app.task
def run_single_spider(spider_name):
    try:
        # Dynamically import the spider class by name
        module_path, class_name = spider_name.rsplit('.', 1)
        spider_module = importlib.import_module(module_path)
        spider_class = getattr(spider_module, class_name)

        # Initialize and start the crawler for the given spider class
        crawler = UrlCrawlerScript(spider_class)
        crawler.start()
        crawler.join()
    except ImportError as e:
        raise ValueError(f"Error importing spider '{spider_name}': {str(e)}")
    except AttributeError:
        raise ValueError(
            f"Spider class '{class_name}' not found in '{module_path}'")
    except Exception as e:
        raise RuntimeError(
            f"An error occurred while running spider '{spider_name}': {str(e)}")
