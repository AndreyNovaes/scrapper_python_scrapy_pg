import scrapy
from ..Generate_urls import Generate_urls
import scrapyProject.items as items
import os

class BuscapeSpider(scrapy.Spider):
  name = "buscape"
  instancia_generate_urls = Generate_urls()
  
  start_urls = instancia_generate_urls.generate_urls_buscape(["celular", "geladeira", 'tv'], 50)

  def parse(self, response):
    products = response.css(".SearchCard_ProductCard_Inner__7JhKb")
    category = response.url.split("/")[3].split("?")[0]

    for product in products:
      item = items.ScrapyprojectItem()

      price_str = product.css("p[data-testid = 'product-card::price']::text").get()
      price_decimal = float(price_str.replace("R$", "").replace(".", "").replace(",", "."))      

      item["description"] = product.css("h2::text").get()
      item["price"] = price_decimal
      item["image"] = product.css("img[src^='https']").attrib["src"]
      item["link"] = Generate_urls.mountUrl("https://www.buscape.com.br", product.css("a::attr(href)").get())
      item["category"] = category
      item["website"] = "Buscape"

      yield item
