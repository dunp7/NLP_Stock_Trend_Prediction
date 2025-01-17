''' 
    This py file represent the whole pipeline of the data 

'''
from crawl_data import * 
from store_data import *
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from tqdm import tqdm

    

KEYWORDS = ["cổ đông lớn", "giao dịch cổ phiểu", "vốn điều lệ", "sàn chứng khoán", "kế hoạch kinh doanh", "chứng khoán",
"công ty con", "cổ phiếu quỹ", "cổ đông", "hội đồng", "giá chào bán", "lợi nhuận quý", "tạm ứng cổ tức",  "thành viên HĐQT",
"công bố"]
# Pre-defined Variables
# KEYWORDS = ['BluechipS', 'CAR', 'CTCK', 'Capital Adequacy Ratio', 'Chính sách tiền tệ', 'Chính sách đất đai', 
#  'Doanh số bán hàng', 'Dự án bất động sản mới', 'ETF', 'Giá bất động sản', 'HOSE', 'Khối lượng giao dịch', 
#  'Lãi suất FED', 'Lãi suất ngân hàng', 'Lãi suất vay mua nhà', 'Lợi nhuận ngân hàng', 'Nợ xấu', 
#  'Pháp lý dự án', 'Phát hành cổ phiếu', 'Quy định ngân hàng', 'Tái cấu trúc ngân hàng', 'biến động thị trường', 
#  'bán ròng', 'bảo hiểm', 'cao su', 'chính sách năng lượng', 'chính sách thuế', 'chính sách tiêu dùng', 
#  'chính sách tài chính', 'chính trị', 'cổ phiếu mới', 'cổ phần', 'cổ tức', 'doanh số bán hàng', 
#  'doanh thu bán lẻ', 'dòng vốn', 'dòng vốn ngoại', 'dòng vốn đầu tư', 'dầu', 'dầu khí', 'dầu mỏ', 
#  'dịch bệnh', 'gang thép', 'giao dịch hoán đổi', 'giao dịch ký quỹ', 'giá dầu', 'giá hàng hóa tiêu dùng', 
#  'giá nguyên liệu', 'giá vàng', 'hoạt động thương mại điện tử', 'hàng không', 'khu công nghiệp', 
#  'khí đốt', 'khối ngoại', 'ký quỹ', 'luật chứng khoán', 'lãi suất', 'lạm phát', 'lợi nhuận', 
#  'lợi nhuận doanh nghiệp', 'margin', 'mua ròng', 'mở rộng thị trường', 'nguồn cung năng lượng', 
#  'ngân hàng thương mại', 'nhà đầu tư', 'nhà đầu tư mới', 'niêm yết', 'nâng lô giao dịch', 'nông nghiệp', 
#  'penny', 'phát hành', 'phát triển thương hiệu', 'quy mô dòng vốn', 'quy định thuế', 'quỹ ETF', 
#  'quỹ đầu tư', 'sàn niêm yết', 'sản phẩm', 'sản xuất công nghiệp', 'sở hữu nước ngoài', 'thanh khoản', 
#  'thanh khoản thị trường', 'thiên tai', 'thuế', 'thép', 'thông lệ quốc tế', 'thị trường chứng khoán', 
#  'thị trường niêm yết', 'trái phiếu', 'trái phiếu doanh nghiệp', 'tài sản ròng', 'tăng trưởng GDP', 
#  'tăng trưởng tiêu dùng', 'tỷ giá hối đoái', 'tỷ trọng', 'vốn CAR', 'vốn hóa', 'xu hướng tiêu dùng', 
#  'xây dựng', 'Điều chỉnh quy hoạch', 'đầu tư cơ sở hạ tầng', 'vốn đầu tư']

WEBLINKS = ['https://www.cafef.vn/']

# Data Pipeline
stock_news_data = []
temp_data_path = os.path.abspath(os.path.join(os.getcwd(), 'temp_data1.csv'))

for keyword in KEYWORDS:
    try:
        keyword_data = Crawling_pipeline(setup_driver(), get_headers(), WEBLINKS[0], keyword, scarping_all_data)
        stock_news_data.extend(keyword_data)

        pd.DataFrame(stock_news_data).to_csv(temp_data_path, index=False, encoding='utf-8')
        print(f"Finished crawling for keyword: {keyword}. Data saved to {temp_data_path}")
    except Exception as e:
        print(f"Error crawling for keyword {keyword}: {e}")



# # Save data
# data_path = os.path.abspath(os.path.join(os.getcwd(), 'data.csv'))
# data = pd.DataFrame(stock_news_data)
# data.to_csv(data_path, index=False, encoding='utf-8')

# # Upload to gg drive
# file_id = upload_to_gg_drive(data_path)
# set_folder_public(FOLDER_ID)
# print(file_id)




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


