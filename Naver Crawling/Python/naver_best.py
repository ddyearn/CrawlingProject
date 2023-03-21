from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
import time
import pyperclip

# 일반 리스트 : 상품명/판매할인가/링크
options = webdriver.ChromeOptions()
options.add_argument('--headless')
UserAgent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0'
options.add_argument('user-agent=' + UserAgent)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://search.shopping.naver.com/best/home?categoryCategoryId=ALL&categoryDemo=A00&categoryRootCategoryId=ALL&chartDemo=A00&chartRank=1&period=P1D&windowCategoryId=20000002&windowDemo=A00&windowRootCategoryId=20000002")

time.sleep(10)

# html 정보 출력
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
f = open("naver_best.html", "w")
f.write(soup.prettify())
f.close()


itemList = []
priceList = []
urlList = []

# lists = driver.find_element(By.CLASS_NAME, 'home_section___JZu3')
lis = driver.find_elements(By.CLASS_NAME, 'imageProduct_item__KZB_F')
for li in lis:
    item = li.find_element(By.CLASS_NAME, 'imageProduct_title__Wdeb1').text
    price = li.find_element(By.CLASS_NAME, 'imageProduct_price__W6pU1').text
    url = li.find_element(By.TAG_NAME, 'a').get_attribute('href')

    itemList.append(item)
    priceList.append(price)
    urlList.append(url)

dic = {'item' : itemList, 'price' : priceList, 'url' : urlList}
Naver_Event_df = pd.DataFrame(dic)
Naver_Event_df.to_csv('./Naver_Best.csv')
driver.quit()