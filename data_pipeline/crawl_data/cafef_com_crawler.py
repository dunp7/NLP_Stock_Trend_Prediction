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
from .utils import setup_driver, get_headers, Crawling_pipeline
import os
import re


'''  CRAWLING PROCESS '''

def search_for_keyword(driver, KEYWORD):
    """
    Function to search for a keyword
    """
    try:
        # Locate the search box container
        search_box_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "CafeF_BoxSearchNew"))
        )

        # Locate the News Category within search box container
        search_filter = WebDriverWait(search_box_container, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "checked"))
        )
        news_search_filter = search_filter.find_element(By.ID, "CafeF_BoxSearch_Type_News")
        news_search_filter.click()

        # Locate the search text box and send keys
        search_input = WebDriverWait(search_box_container, 5).until(
            EC.presence_of_element_located((By.ID, "CafeF_SearchKeyword_News"))
        )
        search_input.send_keys(KEYWORD)
        search_input.send_keys(Keys.RETURN)
    except Exception as e:
        print(f"Error during search_for_keyword: {e}")
        raise



def take_news_href(driver):
    """
    Function to extract news links and titles
    """
    data = []
    try:
        news_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "search-content-wrap"))
        )
        new_containers = news_div.find_elements(By.CLASS_NAME, "item")

        for new in new_containers:
            try:
                news_div = new.find_element(By.CLASS_NAME, "box-category-link-title")
                data.append({
                    "href": news_div.get_attribute("href"),
                    "title": news_div.get_attribute("title")
                })
            except StaleElementReferenceException as stale_ex:
                print("Stale element detected, skipping...")
                continue
    except Exception as e:
        print(f"Error during take_news_href: {e}")
    return data

def normalize_keyword(keyword):
    """
    Prepare a keyword for regex matching.
    Escape special characters and make it case-insensitive.
    """
    return re.escape(keyword)


def is_keyword_in_content(content, keyword):
    """
    Check if a keyword exists in the content using regex.
    """
    pattern = normalize_keyword(keyword)
    return bool(re.search(pattern, content, flags=re.IGNORECASE))

def crawl_news_content(headers, href, keyword):
    """
    Function to crawl news content and check for keywords using regex.
    """
    try:
        response = requests.get(href, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        article_container = soup.find("div", class_="content_cate wp1040")

        if not article_container:
            return "No Content Found", None

        # Publish Date
        date_element = article_container.find("span", class_="pdate")
        publish_date = date_element.get_text(strip=True) if date_element else "Unknown"

        # Content
        content_div = article_container.find("div", class_="contentdetail")
        content = content_div.get_text(strip=True) if content_div else "No Content"

        # Kiểm tra từ khóa trong nội dung với regex
        keyword_in_content = is_keyword_in_content(content, keyword)

        return content, publish_date, keyword_in_content
    except Exception as e:
        print(f"Error crawling content from {href}: {e}")
        return "Error Fetching Content", None, False



def fetch_with_retry(url, headers, retries=3, backoff=5):
    for i in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response
        except Exception as e:
            print(f"Retry {i+1}/{retries}: {e}")
            time.sleep(backoff)
    raise Exception(f"Failed to fetch {url} after {retries} retries")


def save_to_csv_incremental(file_path, data):
    # Kiểm tra nếu file đã tồn tại, ghi thêm không header
    if os.path.exists(file_path):
        pd.DataFrame(data).to_csv(file_path, mode='a', index=False, encoding='utf-8', header=False)
    else:
        pd.DataFrame(data).to_csv(file_path, mode='w', index=False, encoding='utf-8')


def scarping_all_data(driver, headers, keyword):
    """
    Crawling dữ liệu từ trang web và kiểm tra từ khóa trong cả tiêu đề và nội dung.
    """
    news_data = []
    temp_data_path = os.path.abspath(os.path.join(os.getcwd(), 'temp_data.csv'))

    search_for_keyword(driver, keyword)  # Tìm kiếm từ khóa trên trang web
    with tqdm(desc="Scraping News Pages", total=7, unit="page") as pbar:
        for page in range(7):
            try:
                # Lấy danh sách các bài viết trên trang hiện tại
                page_data = take_news_href(driver)

                # Xử lý từng bài viết
                for item in page_data:
                    title_match = is_keyword_in_content(item["title"], keyword)  # Kiểm tra từ khóa trong tiêu đề
                    content, publish_date, content_match = crawl_news_content(headers, item["href"], keyword)  # Kiểm tra trong nội dung
                    
                    # Chỉ lưu bài viết nếu từ khóa khớp trong tiêu đề hoặc nội dung
                    if title_match or content_match:
                        item.update({
                            "publish_date": publish_date,
                            "content": content,
                            "keyword": keyword
                        })
                        news_data.append(item)  # Lưu bài viết khớp
                        print(f"Saved article: {item['title']} (Keyword found in {'title' if title_match else 'content'})")

                # Lưu dữ liệu tạm thời vào file CSV
                save_to_csv_incremental(temp_data_path, news_data)

                # Điều hướng sang trang tiếp theo
                news_div = driver.find_element(By.CLASS_NAME, "search-content-wrap")
                next_button = news_div.find_element(By.CLASS_NAME, "pagination-next")
                next_button.click()
                time.sleep(2)
                pbar.update(1)
            except Exception as e:
                print(f"Error on page {page + 1}: {e}")
                break

    driver.quit()
    return news_data



if __name__ == '__main__':
    pass

    # link = 'https://www.cafef.vn/'
    # key_word = 'Ngân hàng'

    # data= Crawling_pipeline(setup_driver(), get_headers(), link, key_word, scarping_all_data)
# ?    print(data)
    
        
