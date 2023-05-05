import scrapy
from scrapyProject.items.meli_item import MeliItem
from scrapyProject.item_loaders import MeliItemLoader
from scrapyProject.urls_manager import generate_urls_meli, check_url_status

class MeliSpiderSpider(scrapy.Spider):
  name = "meli"
  categories = [
    '/eletrodomesticos/refrigeracao/geladeiras/geladeira',
    '/celulares-telefones/celulares-smartphones/celulares-smartphones',
    '/eletronicos-audio-video/televisores/tv'
    ]
  number_of_pages = 41
  urls = generate_urls_meli(categories, number_of_pages)
  start_urls = check_url_status(urls)

  def parse(self, response):
    products = response.xpath('//li[contains(@class, "ui-search-layout__item")]')
    category = response.url.split('/')[-1].split('_')[0]

    for product in products:
      item_loader = MeliItemLoader(item=MeliItem(), selector=product)

      item_loader.add_css('description', 'h2.ui-search-item__title::text')
      item_loader.add_xpath('image', './/img[contains(@class, "ui-search-result-image__element")]/@data-src | .//img[contains(@class, "ui-search-result-image__element")]/@src')
      item_loader.add_css('link', 'a.ui-search-link::attr(href), img.ui-search-result-image__element::attr(src)')
      price_selector = (
        "span.price-tag.ui-search-price__part:not(.ui-search-price__original-value) > "
        "span.price-tag-amount > "
        "span.price-tag-fraction::text"
      )
      item_loader.add_css('price', price_selector)
      
      item_loader.add_value('category', category)
      item_loader.add_value('website', 'Mercado Livre')

      yield item_loader.load_item()