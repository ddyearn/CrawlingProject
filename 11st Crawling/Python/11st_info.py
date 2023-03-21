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
import csv
from selenium.webdriver import ActionChains


options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('lang=ko_KR')
# options.add_argument("--window-size=10, 200")
UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/111.0.0.0 Safari/537.36'
options.add_argument('user-agent=' + UserAgent)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


# 상품 상세 - 상품명, 판매할인가, 배송비, 별점, 리뷰수, 카테고리
# 웹사이트 열기
driver.get("https://www.11st.co.kr/products/pa/4243449533?inpu=&trTypeCd=22&trCtgrNo=895019")

time.sleep(5)

# html 정보 출력
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
f = open("11st_info.html", "w")
f.write(soup.prettify())
f.close()


info = driver.find_element(By.CLASS_NAME, 'l_product_side_info')

item = info.find_element(By.CLASS_NAME, 'title').text
price = info.find_element(By.CLASS_NAME, 'value').text
delivery = info.find_element(By.XPATH, '//*[@id="layBodyWrap"]/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/dl/div[3]/dt/div/button/strong').text
reviewCount = info.find_element(By.CSS_SELECTOR, '#layBodyWrap > div.l_content > div > div.l_product_cont_wrap > div > div.l_product_view_wrap > div.l_product_summary.l_product_summary_amazon > div.l_product_side_info > div.b_product_info_assist > div > a > strong').text
starscore = info.find_element(By.CLASS_NAME, 'c_seller_grade').text
category = driver.find_element(By.CLASS_NAME, 'c_product_category_path').find_element(By.CLASS_NAME, 'selected').text

f = open('./11st_Item_Info.csv', 'w', newline='')
wr = csv.writer(f)
wr.writerow(['상품명', item])
wr.writerow(['판매원가', price])
wr.writerow(['배송비',delivery])
wr.writerow(['리뷰수',reviewCount])
wr.writerow(['별점',starscore])
wr.writerow(['카테고리',category])
f.close()

# 브라우저 종료
# browser.close() # 현재 탭만 종료
driver.quit() # 전체 브라우저 종료
