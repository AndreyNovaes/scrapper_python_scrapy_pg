from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst
from scrapyProject.utils import handle_meli_compost_category_name, process_base64_image, remove_html_tags_and_whitespaces, remove_currency_symbol, convert_to_float
from scrapyProject.urls_manager import mount_relative_urls_buscape

class BuscapeItemLoader(ItemLoader):
    default_input_processor = MapCompose(remove_html_tags_and_whitespaces)
    default_output_processor = TakeFirst()
    price_in = MapCompose(remove_html_tags_and_whitespaces, remove_currency_symbol, convert_to_float)
    link_in = MapCompose(remove_html_tags_and_whitespaces, mount_relative_urls_buscape)

class MeliItemLoader(ItemLoader):
    default_input_processor = MapCompose(remove_html_tags_and_whitespaces)
    default_output_processor = TakeFirst()
    category_in = MapCompose(remove_html_tags_and_whitespaces, handle_meli_compost_category_name)
    price_in = MapCompose(remove_html_tags_and_whitespaces, convert_to_float)
    link_in = MapCompose(remove_html_tags_and_whitespaces, mount_relative_urls_buscape)
    image_in = MapCompose(remove_html_tags_and_whitespaces, process_base64_image)
    