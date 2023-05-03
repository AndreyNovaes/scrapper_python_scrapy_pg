import os
import subprocess
from dotenv import load_dotenv

def run_command(command, error_message):
  result = subprocess.run(command, shell=True, text=True)
  if result.returncode != 0:
    print(f"Error: {error_message}")
    exit(1)

print("Setting environment variables...")
load_dotenv()

print("Entering scrapyProject...")
os.chdir("scrapyProject")

print("Running buscape spider...")
run_command("scrapy crawl buscape", "Failed to run buscape spider")

print("Running meli spider...")
run_command("scrapy crawl meli", "Failed to run meli spider")

print("Finished running spiders")
