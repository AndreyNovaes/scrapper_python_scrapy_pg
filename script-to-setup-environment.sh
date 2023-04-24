#!/bin/bash

set -e

echo "Updating packages and installing git, python3, and pip..."
sudo yum update -y
sudo yum install -y git python3 python3-pip

GITHUB_REPO_URL="https://github.com/AndreyNovaes/scrapper_python_scrapy_pg.git"
echo "Cloning GitHub repository..."
git clone "$GITHUB_REPO_URL"

echo "Entering repository directory..."
cd scrapper_python_scrapy_pg

echo "creating virtual environment..."
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

echo "Exiting repository directory..."
cd ..

echo "Removing repository directory..."
rm -rf scrapper_python_scrapy_pg
