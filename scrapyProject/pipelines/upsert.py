import uuid
import psycopg2
import os
from dotenv import load_dotenv
from ..utils import count_matching_fields

load_dotenv()

class UpsertPipeline:
  def __init__(self):
    database_url = os.getenv("DATABASE_URL")
    self.conn = psycopg2.connect(database_url)
    self.cur = self.conn.cursor()

  def open_spider(self, spider):
    self.cur.execute("""
      CREATE TABLE IF NOT EXISTS scrapped_data (
      id TEXT PRIMARY KEY,
      category TEXT,
      description TEXT,
      price REAL,
      image TEXT,
      link TEXT,
      website TEXT
    )
    """)
    self.conn.commit()

  def process_item(self, item, spider):
    self.cur.execute("""
      SELECT * FROM scrapped_data
      WHERE category = %s OR description = %s OR website = %s OR image = %s
    """, (item['category'], item['description'], item['website'], item['image']))
    existing_products = self.cur.fetchall()

    matching_product = None
    for product in existing_products:
      product_dict = dict(zip([desc[0] for desc in self.cur.description], product))
      if count_matching_fields(item, product_dict, ['category', 'description', 'price', 'image', 'link', 'website']) >= 4:
        matching_product = product_dict
        break

    if matching_product is None:
      id = str(uuid.uuid4())
      action = "inserted"
      self.cur.execute("""
        INSERT INTO scrapped_data (id, category, description, price, image, link, website)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
      """, (id, item['category'], item['description'], item['price'], item['image'], item['link'], item['website']))
    else:
      action = "updated"
      self.cur.execute("""
        UPDATE scrapped_data
        SET category = %s, description = %s, price = %s, image = %s, link = %s, website = %s
        WHERE id = %s
      """, (item['category'], item['description'], item['price'], item['image'], item['link'], item['website'], matching_product['id']))
    
    self.conn.commit()
    spider.logger.info(f"Item {action}: {item['description']}")
    return item

  def close_spider(self, spider):
    self.conn.close()
