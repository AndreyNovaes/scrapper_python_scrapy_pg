import os

AUTOTHROTTLE_ENABLED = True
ROBOTSTXT_OBEY = False
USER_AGENT = os.getenv("USER_AGENT")

ITEM_PIPELINES = {
    "scrapyProject.pipelines.ScrapyprojectPipeline": 100,
    "scrapyProject.pipelines.SaveToDatabasePipeline": 300,
}

BOT_NAME = "scrapyProject"

SPIDER_MODULES = ["scrapyProject.spiders"]
NEWSPIDER_MODULE = "scrapyProject.spiders"
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
