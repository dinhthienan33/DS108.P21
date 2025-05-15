import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from concurrent.futures import ThreadPoolExecutor
from tornado import concurrent

webdriver_path = "edgedriver_win64/msedgedriver.exe"
service = Service(webdriver_path)
options = Options()

driver = webdriver.Edge(service=service, options=options)

df = pd.read_csv('urls.csv')
# Truy cập cột 'URL' trong DataFrame
urls = df['URL'].tolist()

data = []
i = 0

for url in urls:
    i = i + 1
    print(i,"/329")
    driver.get(url + "&p=10")

    time.sleep(2)
    elements = driver.find_elements(By.XPATH, "//div[@class='prdItem']//a")

    for element in elements:
        # Lấy giá trị của thuộc tính href
        href_value = element.get_attribute("href")

        # Lấy giá sản phẩm
        price_element = element.find_element(By.XPATH, ".//div[@class='price']/strong")
        price = price_element.text.strip()

        data.append({'URL': href_value, 'Price': price})

driver.quit()

# Tạo DataFrame từ dữ liệu
df = pd.DataFrame(data)

# Loại bỏ các giá trị trùng nhau
df_unique = df.drop_duplicates(subset='Price')
df_unique = df_unique.drop('Price', axis=1)
# Lưu DataFrame vào file CSV
df_unique.to_csv('url_final.csv', index=False)