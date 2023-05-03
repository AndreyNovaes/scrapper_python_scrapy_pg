from scrapy.exceptions import DropItem

class RemoveIncompleteItemsPipeline:
  def process_item(self, item, spider):
    necessary_values = ['description', 'price', 'image', 'link', 'category', 'website']
    for value in necessary_values:
      if not item.get(value):
        raise DropItem(f"item dropado por não possuir o valor {value}")
      return item
