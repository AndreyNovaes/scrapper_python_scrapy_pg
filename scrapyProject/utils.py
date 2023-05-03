from w3lib.html import remove_tags

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
  