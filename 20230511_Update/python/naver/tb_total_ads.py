from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pymysql
from bs4 import BeautifulSoup
import time

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import mysql.connector
from urllib.request import urlopen
import pandas as pd
from datetime import datetime
from pandas import DataFrame
import pyperclip
import subprocess
import re

# DB Insert
def insert_data(dbconn, cursor, data) : 
    try : 
        cursor.execute(f"""
            INSERT IGNORE INTO tb_total_ads
            (
                PRODUCT_NAME, PRODUCT_NO, LIST_PRICE, PRICE, TOTAL_PRICE, STAR_SCORE, REVIEW_COUNT,  
                SALE_COMPANY, DELIVERY_PRICE, PRODUCT_URL, DELIVERY_TYPE,
                BRAND_NAME, SALESMAN, PRODUCT_CATEGORY, EVENT, 
                CREATED, UPDATED, UPDATER, COLLECTION_DATE, 
                COMMERCE_TYPE, SEARCH_WORD, ADS_YN
            ) 
            VALUES 
            (
                "{data['product_name']}", "{data['product_no']}", "{data['list_price']}", "{data['price']}",
                "{data['total_price']}", "{data['star_score']}", "{data['review_count']}",
                "{data['sale_company']}", "{data['delivery_price']}", "{data['product_url']}", "{data['delivery_type']}", 
                "{data['brand_name']}", "{data['salesman']}", "{data['category']}", "{data['event']}", 
                "{data['created']}", "{data['updated']}", "{data['updater']}", "{data['collection_date']}", 
                "{data['commerce_type']}", "{data['search_word']}", "{data['ads_yn']}"
            ) 
        """)
    except Exception as e :
        print(f'***** + insert_data error! >> {e}')
    finally : 
        dbconn.commit()
        print('****  상품 insert 완료! ')

class GetData :
    def __init__(self, dbconn, cursor) : 
        self.dbconn = dbconn
        self.cursor = cursor

    def total_ads(self):
        url = 'https://search.shopping.naver.com/search/all?query=즉석밥&cat_id=&frm=NVSHATC'
        driver.get(url=url)
        time.sleep(5)

        div = driver.find_element(By.CSS_SELECTOR, '#content > div.style_content__xWg5l')
        
        list = div.find_element(By.CSS_SELECTOR, 'div.list_basis')
        lis = list.find_elements(By.CLASS_NAME, 'ad')
        
        for li in lis:
            data = {}
            img = li.find_element(By.CSS_SELECTOR, 'div > div.basicList_img_area__AdRY_ > div > a > img').get_attribute('src')
            productUrl = li.find_element(By.CSS_SELECTOR, 'div > div.basicList_img_area__AdRY_ > div > a').get_attribute('href')
            salesman = li.find_element(By.CSS_SELECTOR, 'div > div.basicList_mall_area__faH62 > div.basicList_mall_title__FDXX5 > a.basicList_mall__BC5Xu').text
            category = li.find_element(By.CSS_SELECTOR, 'div > div.basicList_info_area__TWvzp > div.basicList_depth__SbZWF').text

            li.find_element(By.CSS_SELECTOR, 'div > div.basicList_img_area__AdRY_ > div > a').click()
            time.sleep(5)
            driver.switch_to.window(driver.window_handles[-1]) 

            productName = driver.find_element(By.CSS_SELECTOR, '#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._3k440DUKzy > div._1eddO7u4UC > h3').text
            
            try:
                listPrice = driver.find_element(By.CSS_SELECTOR, '#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._3k440DUKzy > div.WrkQhIlUY0 > div > del > span._1LY7DqCnwR').text
                listPrice = listPrice.replace(',', '')
                listPrice = (int)(listPrice, base=0)
            except NoSuchElementException:
                listPrice = 0
            try:
                price = driver.find_element(By.CSS_SELECTOR, '#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._3k440DUKzy > div.WrkQhIlUY0 > div > strong > span._1LY7DqCnwR').text
                price = price.replace(',', '')
                price = (int)(price, base=0)
            except NoSuchElementException:
                price = 0

            deliveryType = driver.find_element(By.CSS_SELECTOR, '#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._1rGSKv6aq_ > div > span:nth-child(1)').text
            deliveryPrice = driver.find_element(By.CSS_SELECTOR, '#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._1rGSKv6aq_ > div > span:nth-child(2)').text
            
            totalPrice = driver.find_element(By.CSS_SELECTOR, '#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._3k440DUKzy > div.WrkQhIlUY0 > div > strong > span._1LY7DqCnwR').text
            totalPrice = totalPrice.replace(',', '')
            totalPrice = (int)(totalPrice, base=0)
            
            starScore = driver.find_element(By.CSS_SELECTOR, '#content > div > div._2-I30XS1lA > div.-g-2PI3RtF > div.NFNlCQC2mv > div:nth-child(2) > strong').text
            starScore = starScore.replace('\n/\n5', '')
            starScore = float(starScore)
            reviewCount = driver.find_element(By.CSS_SELECTOR, '#content > div > div._2-I30XS1lA > div.-g-2PI3RtF > div.NFNlCQC2mv > div:nth-child(1) > a > strong').text
            reviewCount = reviewCount.replace(',', '')
            reviewCount = (int)(reviewCount, base=0)

            productNo = driver.find_element(By.CSS_SELECTOR, '#INTRODUCE > div > div.attribute_wrapper > div > div._2E4i2Scsp4._copyable > table > tbody > tr:nth-child(1) > td:nth-child(2) > b').text
            saleCompany = driver.find_element(By.CSS_SELECTOR, '#INTRODUCE > div > div.attribute_wrapper > div > div._2E4i2Scsp4._copyable > table > tbody > tr:nth-child(2) > td:nth-child(2)').text
            brandName = driver.find_element(By.CSS_SELECTOR, '#INTRODUCE > div > div.attribute_wrapper > div > div._2E4i2Scsp4._copyable > table > tbody > tr:nth-child(2) > td:nth-child(4)').text
            event = driver.find_element(By.CSS_SELECTOR, '#INTRODUCE > div > div.attribute_wrapper > div > div._2E4i2Scsp4._copyable > table > tbody > tr:nth-child(3) > td:nth-child(2)').text

            searchWord = '즉석밥'
            adsYn = 'Y'
            commerceType = 'NAVER'
            created = datetime.now()
            updated = datetime.now()
            updater = 'root'
            collection_date = datetime.now()

            driver.close()
            driver.switch_to.window(driver.window_handles[0]) 
            time.sleep(5)
            
            data = {
                'product_no': productNo,
                'product_name':productName,
                'list_price': listPrice,
                'price':price,
                'total_price':totalPrice,
                'star_score':starScore,
                'review_count':reviewCount,
                'sale_company':saleCompany,
                'delivery_price':deliveryPrice,
                'product_url':productUrl,
                'delivery_type':deliveryType,
                'brand_name':brandName,
                'salesman':salesman,
                'category':category,
                'event':event,
                'created':created,
                'updated':updated,
                'updater':updater,
                'collection_date':collection_date,
                'commerce_type':commerceType,
                'search_word':searchWord,
                'ads_yn':adsYn
            }

            insert_data(self.dbconn, self.cursor, data)


# chrome setting
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches",["enable-automation"])

options.add_argument('--disable-gpu')
options.add_argument('lang=ko_KR')
UserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/111.0.0.0 Safari/537.36'
options.add_argument('user-agent=' + UserAgent)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.implicitly_wait(10)

# Maria DB 연결
conn = pymysql.connect(host='127.0.0.1', port=3307, user='syeon', password='muze2005', db='cpdb', charset='utf8')
cur = conn.cursor()

GetData = GetData(conn, cur)
GetTotalAds = GetData.total_ads()

conn.close()
driver.quit()


'''
# tb_total_ads
# 광고 리스트 : 상품명/판매원가/배송비/카테고리

driver.get("https://search.shopping.naver.com/search/all?query=즉석밥&cat_id=&frm=NVSHATC")
time.sleep(5)

# html 정보 출력
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
f = open("naver_ad.html", "w")
f.write(soup.prettify())
f.close()

# csv 저장


# mariaDB 저장
lists = driver.find_elements(By.CSS_SELECTOR, '#content > div.style_content__xWg5l > div.list_basis > div > div:nth-child(1) > div')
pn = 0
for li in lists:
    pn += 1
    item = li.find_element(By.CLASS_NAME, 'basicList_title__VfX3c').text
    price = li.find_element(By.CLASS_NAME, 'price_price__LEGN7').text
    price = price.replace(',', '').replace('원', '')
    delivery = li.find_element(By.CLASS_NAME, 'price_delivery__yw_We').text
    del_free = "무료"
    if del_free in delivery:
        delivery = "0"
    category = li.find_element(By.CLASS_NAME, 'basicList_depth__SbZWF').text
    url = li.find_element(By.TAG_NAME, 'a').get_attribute('href')

    insert = "INSERT INTO tb_total_ads (product_name, product_no, price, delivery_price, product_category, product_url) VALUES('"+item+"', '"+str(pn)+"', '"+price+"', '"+delivery+"', '"+category+"', '"+url+"') "
    update = "ON DUPLICATE KEY UPDATE price='"+price+"', delivery_price='"+delivery+"', product_category='"+category+"', product_url='"+url+"'"
    sql = insert + update

cur.execute(sql)
conn.commit()

conn.close()

# 7. 브라우저 종료
# browser.close() # 현재 탭만 종료
driver.quit() # 전체 브라우저 종료


user_id = 'bestsy777'
user_pw = 'muze2005;'

# 네이버쇼핑 이동
driver.get('https://shopping.naver.com/home')


# 로그인
elem = driver.find_element(By.CLASS_NAME,'gnb_btn_login')
elem.click()
# 자바스크립트로 입력
driver.execute_script(
    f"document.querySelector('input[id=\"id\"]').setAttribute('value', '{user_id}')"
)
time.sleep(1)
driver.execute_script(
    f"document.querySelector('input[id=\"pw\"]').setAttribute('value', '{user_pw}')"
)
# 로그인 버튼 클릭
driver.find_element(By.ID,'log.login').click()
time.sleep(2)
'''