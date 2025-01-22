# # Dataframe
import pandas as pd

# Web Crawling
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Other
import time
from tqdm import tqdm
from utils import get_headers, setup_driver
import urllib.parse

class thoibaotaichinhvietnam_crawl():

    def __init__(self):
        self.driver = setup_driver()
        self._data = {
            "href": [], 
            "title" : [],
            "publish_date" : [],
            "content": [],
            "keyword": []
        }
    
    def get_data(self):
        return self._data

    def decode_keyword(self, keyword):
        return urllib.parse.quote(keyword)
    
         
    def scraping_news_link(self, news):
        
        link_element =  news.find_element(By.CLASS_NAME, 'article-thumb')
        href = link_element.get_attribute('href')
        title = link_element.get_attribute('title')

        time_element = news.find_element(By.CLASS_NAME, 'article-meta')
        time = time_element.find_element(By.CLASS_NAME, 'format_time').text
        date = time_element.find_element(By.CLASS_NAME, 'format_date').text
        publish_date = f"{time} {date}"



        # headers = get_headers()
        # response = requests.get(href, headers=headers)
        # soup = BeautifulSoup(response.content, 'html.parser')

        # article_container = soup.find("div",class_ = "min-w-0")
        # if article_container:
        #     content = article_container.find("div", class_ = "relative flex flex-col").get_text(strip=True)
        # else:
        #     content = "No content Found"
        content = 0

        return href, title, publish_date, content


    def scaping_one_page(self, keyword):

        pointer = self.driver.find_element(By.CLASS_NAME, "w799")
        news_articles = pointer.find_element(By.CLASS_NAME, "cat-listing")\
                                    .find_element(By.CLASS_NAME, "cat-content")\
                                .find_elements(By.CLASS_NAME, "article")

        time.sleep(1)
        for news in news_articles: 
            href,title,publish_date,content = self.scraping_news_link(news)
            self._data['href'].append(href)
            self._data['title'].append(title)
            self._data['publish_date'].append(publish_date)
            self._data['content'].append(content)
            self._data['keyword'].append(keyword)


    def scraping_news_with_keyword(self, keyword, nums_pages= 10):

        # Access to news with predefined keyword
        self.driver.get(f"https://thoibaotaichinhvietnam.vn/search_enginer.html?p=search&q={self.decode_keyword(keyword)}")
        time.sleep(2)

        with tqdm(desc="Scraping News Pages", total=nums_pages ,unit="page") as pbar:
            for _ in range(nums_pages):
                self.scaping_one_page(keyword)
                pbar.update(1)
                # Move to next page
                pointer = self.driver.find_element(By.CLASS_NAME, "w799")
                pointer.find_element(By.CLASS_NAME, "__MB_ARTICLE_PAGING").find_element(By.XPATH, '//a[text()=">"]').click()


        print(f"Finish crawling with {keyword}")

if __name__ == '__main__':

    crawler = thoibaotaichinhvietnam_crawl()
    crawler.scraping_news_with_keyword("Vàng", 2)
    
    data = crawler.get_data()
    print(data)
    data = pd.DataFrame(data)
    print(data.head())
    data.to_csv("data.csv", index=False, encoding='utf-8')
