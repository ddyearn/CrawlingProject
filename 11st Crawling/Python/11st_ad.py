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

# 광고 리스트 - 상품명, 판매할인가, 배송비, 별점, 리뷰수, 링크
# 웹사이트 열기
driver.get("https://search.11st.co.kr/Search.tmall?kwd=%EC%A6%89%EC%84%9D%EB%B0%A5")

time.sleep(5)

# html 정보 출력
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
f = open("11st_ad.html", "w")
f.write(soup.prettify())
f.close()


itemList = []
priceList = []
deliveryFeeList = []
starRateList = []
reviewCountList = []
urlList = []

adList = driver.find_elements(By.CLASS_NAME, 'help_ad')
for ad in adList:
    lists = ad.find_element(By.XPATH, '..').find_element(By.XPATH, '..')
    lis = lists.find_elements(By.CLASS_NAME, 'c_card')


    for li in lis:
        item = li.find_element(By.CLASS_NAME, 'c_prd_name').text
        price = li.find_element(By.CLASS_NAME, 'price').text
        deliveryFee = li.find_element(By.CLASS_NAME, 'delivery').text
        try :
            starRate = li.find_element(By.CLASS_NAME, 'c_seller_grade grade_90').text
            reviewCount = li.find_element(By.CLASS_NAME, 'c_review').text
        except :
            starRate = ''
            reviewCount = ''
        url = li.find_element(By.TAG_NAME, 'a').get_attribute('href')

        itemList.append(item)
        priceList.append(price)
        deliveryFeeList.append(deliveryFee)
        starRateList.append(starRate)
        reviewCountList.append(reviewCount)
        urlList.append(url)

dic = {'item' : itemList, 'price' : priceList, 'delivery fee' : deliveryFeeList, 'star rate' : starRateList, 'review count' : reviewCountList, 'url' : urlList}
Naver_Event_df = pd.DataFrame(dic)
Naver_Event_df.to_csv('./11st_Ad.csv')

# 브라우저 종료
# browser.close() # 현재 탭만 종료
driver.quit() # 전체 브라우저 종료