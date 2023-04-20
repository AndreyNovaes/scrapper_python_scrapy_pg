import scrapy
import scrapyProject.items as items

from ..Generate_urls import Generate_urls

class MeliSpiderSpider(scrapy.Spider):
  name = "meli"
  instancia_generate_urls = Generate_urls()
  categories = [
    '/eletrodomesticos/refrigeracao/geladeiras/geladeira',
    '/celulares-telefones/celulares-smartphones/celulares-smartphones',
    '/eletronicos-audio-video/televisores/tv'
    ]
  
  start_urls = instancia_generate_urls.generate_urls_meli(categories, 50)

  def parse(self, response):
    products = response.xpath('//li[contains(@class, "ui-search-layout__item")]')
    category = response.url.split('/')[-1].split('_')[0]

    for product in products:
      item = items.ScrapyprojectItem()
      
      price_str = product.css("span.price-tag-amount > span.price-tag-fraction::text").get()
      price_decimal = float(price_str.replace(".", "").replace(",", "."))
      
      item["image"] = product.css("img.ui-search-result-image__element::attr(data-src)").get()
      item["price"] = price_decimal
      item["description"] = product.css("h2.ui-search-item__title::text").get()
      item["link"] = product.css("a.ui-search-link::attr(href)").get()
      item["website"] = "Mercado Livre"
      
      if category == "celulares-smartphones":
        item["category"] = "celular"
      else:
        item["category"] = category

      yield item