from scrapy import Item, Field

class BuscapeItem(Item):
    description = Field()
    image = Field()
    link = Field()
    price = Field()
    category = Field()
    website = Field()
