from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time

webdriver_path = "edgedriver_win64/msedgedriver.exe"
service = Service(webdriver_path)
options = Options()

driver = webdriver.Edge(service=service, options=options)

url = "https://www.thegioididong.com/may-doi-tra/laptop?pi=17"

driver.get(url)

time.sleep(15)

elements = driver.find_elements(By.XPATH, "//div[@class='prdItem']//a")
url_sp = []

for element in elements:
    # Lấy giá trị của thuộc tính href
    href_value = element.get_attribute("href")
    url_sp.append(href_value)

print(len(url_sp))

driver.quit()

df = pd.DataFrame(url_sp, columns=["URL"])

# Lưu DataFrame thành tệp CSV
df.to_csv("urls.csv", index=False)