#!/bin/bash
echo "creating vitual environment..."
python3 -m venv venv

echo "Entering virtual environment..."
source venv/bin/activate

echo "Setting environment variables..."
if [ -f .env ]; then
  while IFS= read -r line; do
    if [[ ! $line =~ ^# && $line ]]; then
      IFS="=" read -r key value <<< "$line"
      value="${value%\"}"
      value="${value#\"}"
      export "$key=$value"
    fi
  done < .env
else
  echo "No .env file found. Exiting."
  exit 1
fi

echo "Installing requirements..."
pip install -r requirements.txt

echo "Entering scrapyProject..."
cd scrapyProject

echo "Running meli spider..."
scrapy crawl meli

echo "Running buscape spider..."
scrapy crawl buscape

echo "Finished running spiders, exiting virtual environment..."
deactivate
