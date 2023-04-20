import os

class Generate_urls:
  def __init__(self):
    pass

  @staticmethod
  def generate_urls_meli(categoriesLinks, number_of_pages):
#  url exemplo https://lista.mercadolivre.com.br/eletrodomesticos/refrigeracao/geladeiras/geladeira_Desde_1000_NoIndex_True
# categoriesLinks vai receber um array do tipo ['/eletrodomesticos/refrigeracao/geladeiras/geladeira', ...]
# desde_1 = primeira página, desde_51 = segunda página, desde_101 = terceira página e assim por diante
    BASE_URL = "https://lista.mercadolivre.com.br"
    urls = []
    # https://lista.mercadolivre.com.br/eletrodomesticos/refrigeracao/geladeiras/geladeira_NoIndex_True
    for category in categoriesLinks:
      for page_number in range(1, number_of_pages + 1):
        if page_number == 1:
          urls.append(f"{BASE_URL}{category}_NoIndex_True")
        else:
          urls.append(f"{BASE_URL}{category}_Desde_{(page_number - 1) * 50 + 1}_NoIndex_True")
    return urls

  @staticmethod
  def generate_urls_buscape(categories, number_of_pages):
    # Recebe 2 parametros, um array de categorias e o número de páginas que serão 'scrapadas'
      BASE_URL = "https://www.buscape.com.br"
      urls = []
      for page_number in range(1, number_of_pages + 1):
          for category in categories:
              urls.append(f"{BASE_URL}/{category}?page={page_number}")
      return urls
  @staticmethod
  def mountUrl(website, linkExtracted):
    # some links are already complete, so we just return them
    if linkExtracted.startswith("https://www.buscape.com.br"):
      return linkExtracted
    # some links are incomplete, so we need to mount them
    # example: linkExtracted = /celular/smartphone-apple-iphone-12-128gb-ios?_lc=11
    # example: website = https://www.buscape.com.br
    # result: https://www.buscape.com.br/celular/smartphone-apple-iphone-12-128gb-ios?_lc=11
    return website + linkExtracted
