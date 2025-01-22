''' 
    This py file represent the whole pipeline of the data 

'''
from crawl_data import * 
from store_data import *
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from tqdm import tqdm


    


# Pre-defined Variables
KEYWORDS = [
    # "Lãi suất ngân hàng", "Chính sách tiền tệ", "Lợi nhuận ngân hàng", "Phát hành cổ phiếu",\
    # "Tái cấu trúc ngân hàng", "Nợ xấu", "Quy định ngân hàng",\
    # "Chính sách đất đai", "Giá bất động sản", " Lãi suất vay mua nhà", "Dự án bất động sản mới",\
    # "Điều chỉnh quy hoạch", "Pháp lý dự án",\
    # "Doanh số bán hàng", "doanh số bán hàng", "mở rộng thị trường", "hoạt động thương mại điện tử", "tăng trưởng tiêu dùng",\
    # "giá nguyên liệu", "chính sách thuế", "sản xuất công nghiệp", "các dự án mở rộng sản xuất",\
    # "đầu tư cơ sở hạ tầng", \
    # "giá dầu", "khí đốt", "chính sách năng lượng", "đầu tư vào hạ tầng năng lượng", "nguồn cung năng lượng",\
    "giá hàng hóa tiêu dùng", "doanh thu bán lẻ", "chính sách tiêu dùng", "phát triển thương hiệu", "xu hướng tiêu dùng"
    
    ]
WEBLINKS = ['https://www.cafef.vn/']



# Data Pipeline
stock_news_data = []
for keyword in KEYWORDS:
    stock_news_data.extend(Crawling_pipeline(setup_driver(), get_headers(), WEBLINKS[0], keyword, scarping_all_data))
    print(f"Finished: {keyword}")


# Save data
data_path = os.path.abspath(os.path.join(os.getcwd(), 'data.csv'))
data = pd.DataFrame(stock_news_data)
data.to_csv(data_path, index=False, encoding='utf-8')

# Upload to gg drive
file_id = upload_to_gg_drive(data_path)
set_folder_public(FOLDER_ID)
print(file_id)




# Read data -- with other user
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# FOLDER_ID = '1vsLkkxsR5dHemeh7wPyGYoKIvA2xIT-1'
# SECRET_FILE = os.path.join(BASE_DIR, '..', '..', 'dunp1710_client_secrets.json')
# FILE_ID = '1eSnLAt-pfIvpxtU_YABIxbjvaBLpktKU'

# google_auth = GoogleAuth()
# google_auth.LoadClientConfigFile(SECRET_FILE)
# google_auth.LocalWebserverAuth()
# drive_app = GoogleDrive(google_auth)

# # Create a file object using the file_id
# file = drive_app.CreateFile({'id': FILE_ID})

# # Download the file to the local environment
# local_filename = os.path.join(BASE_DIR, 'downloaded_file.csv')
# file.GetContentFile(local_filename)
# print(f'File downloaded to {local_filename}')


