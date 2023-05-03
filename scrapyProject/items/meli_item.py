from scrapy import Item, Field

class MeliItem(Item):
    description = Field()
    image = Field()
    link = Field()
    price = Field()
    category = Field()
    website = Field()
