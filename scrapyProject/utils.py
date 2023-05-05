from w3lib.html import remove_tags  
import base64
import os
import uuid

def remove_currency_symbol(value):
  return value.replace('R$', '')

def convert_to_float(value):
  value = value.replace('.', '').replace(',', '.')
  return float(value)

def remove_html_tags_and_whitespaces(value):
  return remove_tags(value).strip()

def count_matching_fields(item1, item2, fields):
  count = 0
  for field in fields:
    if item1.get(field) == item2.get(field):
      count += 1
  return count

def handle_meli_compost_category_name(category):
  if category == "celulares-smartphones":
    return "celular"
  else:
    return category

def process_base64_image(image_data_base64):
  if image_data_base64.startswith('data:image/'):
    header, image_data_base64 = image_data_base64.split(',', 1)
    image_format = header.split(';')[0].split('/')[1]

    image_data = base64.b64decode(image_data_base64)

    images_path = 'images'
    if not os.path.exists(images_path):
      os.makedirs(images_path)

    image_filename = f"{uuid.uuid4()}.{image_format}"
    image_filepath = os.path.join(images_path, image_filename)
    with open(image_filepath, 'wb') as f:
      f.write(image_data)
      return image_filepath
  return image_data_base64
