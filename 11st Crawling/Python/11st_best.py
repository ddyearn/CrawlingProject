from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
import time
import pyperclip


options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('lang=ko_KR')
# options.add_argument("--window-size=10, 200")
UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/111.0.0.0 Safari/537.36'
options.add_argument('user-agent=' + UserAgent)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 베스트 리스트 - 상품명, 판매할인가, 배송비, 링크
# 웹사이트 열기
driver.get("https://www.11st.co.kr/browsing/BestSeller.tmall?method=getBestSellerMain&xfrom=main^gnb#pageNum%%4")

time.sleep(5)

# html 정보 출력
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
f = open("11st_best.html", "w")
f.write(soup.prettify())
f.close()


itemList = []
priceList = []
deliveryFeeList = []
urlList = []

lists = driver.find_elements(By.CLASS_NAME, 'ranking_pd')


for li in lists:
    item = li.find_element(By.TAG_NAME, 'p').text
    price = li.find_element(By.CLASS_NAME, 'sale_price').text
    deliveryFee = li.find_element(By.CLASS_NAME, 's_flag').text
    url = li.find_element(By.TAG_NAME, 'a').get_attribute('href')

    itemList.append(item)
    priceList.append(price)
    deliveryFeeList.append(deliveryFee)
    urlList.append(url)

dic = {'item' : itemList, 'price' : priceList, 'delivery fee' : deliveryFeeList, 'url' : urlList}
Naver_Event_df = pd.DataFrame(dic)
Naver_Event_df.to_csv('./11st_Best.csv')

# 브라우저 종료
# browser.close() # 현재 탭만 종료
driver.quit() # 전체 브라우저 종료
