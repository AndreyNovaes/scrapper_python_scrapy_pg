#!/bin/bash
echo "creating vitual environment..."
python3 -m venv venv

echo "Entering virtual environment..."
source venv/bin/activate

echo "Verifying environment variables..."
echo "DATABASE_URL: $DATABASE_URL"
echo "USER_AGENT: $USER_AGENT"

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
