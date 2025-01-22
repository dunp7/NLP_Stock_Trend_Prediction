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




'''  CRAWLING PROCESS '''

def search_for_keyword(driver, KEYWORD):
    """
    Function to search for a keyword

    Attributes:
        - driver: Driver setup for Selenium
        - keyword: Keyword for searching

    """
    # Locate the seach box container
    search_box_container = driver.find_element(By.ID, "CafeF_BoxSearchNew")

    ## Locate the News Category within seach box container
    search_filter = search_box_container.find_element(By.CLASS_NAME, "checked")
    news_search_filter = search_filter.find_element(By.ID, "CafeF_BoxSearch_Type_News")
    news_search_filter.click()
    time.sleep(5)
    ## Locate the search text box and send keys
    search_input = search_box_container.find_element(By.ID, "CafeF_SearchKeyword_News")
    search_input.send_keys(KEYWORD)
    search_input.send_keys(Keys.RETURN)
    time.sleep(5)


def take_news_href(driver):
    """
    Function to crawl all the news links
    Attributes:
        - driver: Driver setup for Selenium
    """
    # Locate the element that contain all the news and its information
    news_div = driver.find_element(By.CLASS_NAME, "search-content-wrap")
    ## Take all the news elements within the news div
    new_containers = news_div.find_elements(By.CLASS_NAME, "item")
    data = []
    for new in new_containers:
        new_data = {}
        # news div
        news_div = new.find_element(By.CLASS_NAME, "box-category-link-title")
        new_data["href"] = news_div.get_attribute("href")
        new_data["title"] = news_div.get_attribute("title")
        
        data.append(new_data)

    return data

def crawl_news_content(headers,href):
    """
    Function to crawl news content

    Attributes:
        - headers: Headers for requests
        - href: Link of the news

    """

    response = requests.get(href, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    article_container = soup.find("div",class_ = "content_cate wp1040")
    if article_container:
      #Publish Date
      date_element = article_container.find("span", class_ ="pdate").get_text(strip=True)
      # Content
      content_div = article_container.find("div", class_ = "contentdetail")
      content = content_div.get_text(strip=True)
      return content, date_element
    
    else:
      return "No Content Found", None


def scarping_all_data(driver, headers, keyword):
    """
    A function represent data pipeline for CafeF Crawling

    Attributes: 
        - driver: Driver setup for Selenium
        - headers: Headers for requests
        - keyword: Keyword for searching
    """
    news_data = []
    """ Send Input Keys """
    search_for_keyword(driver, keyword)

    """ Take All News Links """
    with tqdm(desc="Scraping News Pages", total=7 ,unit="page") as pbar:
       for page in range(7):

            # Take all news links from the current page
            news_data.extend(take_news_href(driver))
            """ Crawling Each Page Href Content """
            for ind in range(len(news_data)):
                content, publish_date = crawl_news_content(headers, news_data[ind]["href"])
                news_data[ind]["publish_date"] = publish_date
                news_data[ind]["content"] = content
                news_data[ind]["keyword"] = keyword

            """ Scroll to next page  """
            # Try to navigate to the next page
            try:
                news_div = driver.find_element(By.CLASS_NAME, "search-content-wrap")
                next_button = news_div.find_element(By.CLASS_NAME, "pagination-next")
                next_button.click()
                
                time.sleep(2)  
                # Update the progress bar by one page
                pbar.update(1)
            except Exception as e:
                print("No more pages or error navigating to the next page.")
                break
  

    driver.quit()
    return news_data



if __name__ == '__main__':
    pass

    # link = 'https://www.cafef.vn/'
    # key_word = 'Ngân hàng'

    # data= Crawling_pipeline(setup_driver(), get_headers(), link, key_word, scarping_all_data)
# ?    print(data)
    
        
