import requests
import logging

logging.basicConfig(level=logging.INFO)

def generate_urls_meli(categories_links, number_of_pages):
  """
  Generate Mercado Livre URLs what will be scraped.
  :param categories_links: List of category related links
  :param number_of_pages: Number of pages to scrape for each category
  :return: List of URLs to be scraped
  Example:
  >>> categories_links = [
  ...   '/eletrodomesticos/refrigeracao/geladeiras/geladeira',
  ]
  >>> number_of_pages = 2
  >>> generate_urls_meli(categories_links, number_of_pages)
  ['https://lista.mercadolivre.com.br/eletrodomesticos/refrigeracao/geladeiras/geladeira_NoIndex_True',
  'https://lista.mercadolivre.com.br/eletrodomesticos/refrigeracao/geladeiras/geladeira_Desde_51_NoIndex_True']
  """
  BASE_URL = "https://lista.mercadolivre.com.br"
  urls = []
  for category in categories_links:
    for page_number in range(1, number_of_pages + 1):
      if page_number == 1:
        url = f"{BASE_URL}{category}_NoIndex_True"
      else:
        url = f"{BASE_URL}{category}_Desde_{(page_number - 1) * 50 + 1}_NoIndex_True"
      urls.append(url)
  return urls

def generate_urls_buscape(categories, number_of_pages):
  """
  Generate Buscape URLs to be scraped.
  :param categories_links: List of category links
  :param number_of_pages: Number of pages to scrape for each category
  :return: List of URLs to be scraped
  """
  BASE_URL = "https://www.buscape.com.br"
  urls = []
  for page_number in range(1, number_of_pages + 1):
    for category in categories:
      urls.append(f"{BASE_URL}/{category}?page={page_number}")
  return urls

def mount_relative_urls_buscape(link_extracted):
  """
  Verify if the URL is relative(/path) or abs(http://) and mount relative links and returns it as absolute links.
  :param link: Relative link
  :return: Absolute link
  """
  BASE_URL = "https://www.buscape.com.br"

  if link_extracted.startswith("/"):
    return f"{BASE_URL}{link_extracted}"
  else:
    return link_extracted

def check_url_status(urls):
  """
  Check the HTTP status codes for a list of URLs and return only the URLs with a 200 status code.
  :param urls: List of URLs to be checked
  :return: List of URLs with a 200 status code
  """
  valid_urls = []
  invalid_urls = []

  for url in urls:
    try:
      response = requests.head(url, timeout=10)
      status_code = response.status_code

      if str(status_code).startswith("2") or str(status_code).startswith("3"):
        valid_urls.append(url)
      else:
        invalid_urls.append(url)
        logging.warning(f"Invalid URL '{url}' with status code {response.status_code}")

    except requests.RequestException as e:
      invalid_urls.append(url)
      logging.error(f"Request error for URL '{url}': {e}")

  total_urls = len(urls)
  valid_percentage = (len(valid_urls) / total_urls) * 100
  logging.info(f"Percentage of accepted URLs: {valid_percentage:.2f}%")

  return valid_urls
