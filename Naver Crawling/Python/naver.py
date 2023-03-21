from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
import time
import pyperclip

# 행사 리스트 : 상품명/판매할인가/할인율/링크
options = webdriver.ChromeOptions()
options.add_argument('--headless')
UserAgent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0'
options.add_argument('user-agent=' + UserAgent)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://plusdeal.naver.com/?sort=1")

time.sleep(10)

# 6. html 정보 출력
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
f = open("naver_event.html", "w")
f.write(soup.prettify())
f.close()


itemList = []
priceList = []
discountRateList = []
urlList = []

lists = driver.find_elements(By.CLASS_NAME, 'productCard_product_card_view__yt7Ji')
count = 1

for li in lists:
    if count>100:
        break
    count += 1
    item = li.find_element(By.CLASS_NAME, 'productCard_title__aMA_D').text
    price = li.find_element(By.CLASS_NAME, 'productCard_price__2waKK').text
    discountRate = li.find_element(By.CLASS_NAME, 'productCard_discount__tupNR').text
    url = li.find_element(By.TAG_NAME, 'a').get_attribute('href')

    itemList.append(item)
    priceList.append(price)
    discountRateList.append(discountRate)
    urlList.append(url)

dic = {'item' : itemList, 'price' : priceList, 'discountRate' : discountRateList, 'url' : urlList}
Naver_Event_df = pd.DataFrame(dic)
Naver_Event_df.to_csv('./Naver_Event.csv')
driver.quit()