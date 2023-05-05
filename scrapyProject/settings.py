from fake_useragent import UserAgent

ua = UserAgent()

USER_AGENT = ua.random
AUTOTHROTTLE_ENABLED = True
ROBOTSTXT_OBEY = False
DOWNLOAD_TIMEOUT = 10
DOWNLOAD_DELAY = 2
CONCURRENT_REQUESTS = 32
RETRY_TIMES = 3


ITEM_PIPELINES = {
    'scrapyProject.pipelines.RemoveIncompleteItemsPipeline': 100,
    'scrapyProject.pipelines.UpsertPipeline': 200,
}

BOT_NAME = "scrapyProject"

SPIDER_MODULES = ["scrapyProject.spiders"]
NEWSPIDER_MODULE = "scrapyProject.spiders"
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
