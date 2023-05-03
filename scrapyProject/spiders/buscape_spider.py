import scrapy
from scrapyProject.items.buscape_item import BuscapeItem
from scrapyProject.item_loaders import BuscapeItemLoader
from scrapyProject.urls_manager import generate_urls_buscape, check_url_status

class BuscapeSpider(scrapy.Spider):
  name = "buscape"
  categories = ["celular", "tv", "geladeira"]
  number_of_pages = 41
  urls = generate_urls_buscape(categories, number_of_pages)
  start_urls = check_url_status(urls)

  def parse(self, response):
    products = response.css(".SearchCard_ProductCard_Inner__7JhKb")
    category = response.url.split("/")[3].split("?")[0]

    for product in products:
      item_loader = BuscapeItemLoader(item=BuscapeItem(), selector=product)
      item_loader.add_css('description', 'h2::text')
      item_loader.add_css('image', 'img[src^="https"]::attr(src)')
      item_loader.add_css('price', "p[data-testid = 'product-card::price']::text")
      item_loader.add_css('link', 'a::attr(href)')

      item_loader.add_value('category', category)
      item_loader.add_value('website', 'Buscape')

      yield item_loader.load_item()
