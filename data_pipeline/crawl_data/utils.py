# Dataframe
import pandas as pd

# Web Crawling
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# Other
from datetime import datetime, timedelta
import pytz
import time

def get_headers():
    """
    Define Headers for Request

    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    return headers

def parse_date(day):
    current_time = datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
    if 'giờ' in day:
        hours_ago = int(day.split(' ')[0]) 
        return current_time - timedelta(hours=hours_ago)
    else:
        return day 

def setup_driver():
    """
    Function to set up driver for Selenium
    """
    options = Options()
    # options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--remote-debugging-port=9222")  # Enable remote debugging
    driver = webdriver.Chrome(options=options)

    return driver



def Crawling_pipeline(driver, header, website_link, keyword, main_scraping):
    """
    Function to crawl data from end-to-end

    Attributes:
        - driver: Driver setup for Selenium
        - header: Headers for requests

        - website_link: Link of the website
        - keyword: Keyword for searching

        - main_scraping: Scraping Function for each website
    """
    # Access to website 
    driver.get(website_link)
    time.sleep(5)

    # Crawl data
    data = main_scraping(driver, header, keyword)
    
    return data
