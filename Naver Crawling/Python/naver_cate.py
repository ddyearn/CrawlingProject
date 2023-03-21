from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
import time

# 카테고리 리스트 : 상품명/판매원가/카테고리
options = webdriver.ChromeOptions()
options.add_argument('--headless')
UserAgent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0'
options.add_argument('user-agent=' + UserAgent)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://search.shopping.naver.com/search/category/100007953")
time.sleep(10)

# html 정보 출력
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
f = open("naver_cate.html", "w")
f.write(soup.prettify())
f.close()

itemList = []
priceList = []
categoryList = []
urlList = []

lists = driver.find_elements(By.CLASS_NAME, 'basicList_item__0T9JD')

for li in lists:
    item = li.find_element(By.CLASS_NAME, 'basicList_title__VfX3c').text
    price = li.find_element(By.CLASS_NAME, 'price_price__LEGN7').text
    category = li.find_element(By.CLASS_NAME, 'basicList_depth__SbZWF').text
    url = li.find_element(By.TAG_NAME, 'a').get_attribute('href')

    itemList.append(item)
    priceList.append(price)
    categoryList.append(category)
    urlList.append(url)

dic = {'item' : itemList, 'price' : priceList, 'category' : categoryList, 'url' : urlList}
Naver_Cate_df = pd.DataFrame(dic)
Naver_Cate_df.to_csv('./Naver_Category.csv')
driver.quit()