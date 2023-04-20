from scrapy.exceptions import DropItem
import uuid
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# remove os elementos que não possuem os valores necessários
class ScrapyprojectPipeline:
  def process_item(self, item, spider):
    if not item['description'] or not item['price'] or not item['image'] or not item['link'] or not item['category'] or not item['website']:
      raise DropItem("item dropado por não possuir os valores necessários")
    else:
      return item
    
class SaveToDatabasePipeline:
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
        SELECT id FROM scrapped_data
        WHERE category = %s AND description = %s AND website = %s AND image = %s
      """, (item['category'], item['description'], item['website'], item['image']))
      productAlreadyExists = self.cur.fetchone()
      spider.logger.info(f"productAlreadyExists: {productAlreadyExists}")

      if productAlreadyExists is None:
        id = str(uuid.uuid4())
        self.cur.execute("""
          INSERT INTO scrapped_data (id, category, description, price, image, link, website)
          VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (id, item['category'], item['description'], item['price'], item['image'], item['link'], item['website']))
        self.conn.commit()
        spider.logger.info(f"Item inserted: {item['description']}")
      else:
        spider.logger.info(f"Duplicate item found, removing from memory...")

      return item

    def close_spider(self, spider):
        self.conn.close()

