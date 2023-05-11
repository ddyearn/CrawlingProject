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
            INSERT IGNORE INTO total_category
            ( COMMERCE_TYPE, MAIN, MID, SUB ) 
            VALUES 
            ( "{data['commerce_type']}", "{data['main']}", "{data['mid']}", "{data['sub']}" ) 
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

    def total_category(self):
        url = 'https://search.shopping.naver.com/search/category/100007953'
        driver.get(url=url)
        time.sleep(5)

        commerceType = 'NAVER'

        driver.find_element(By.CSS_SELECTOR, '#wrap > div._gnb_gnb_2C24o > div._gnb_header_area_150KE > div > div._gnbLogo_gnb_logo_3eIAf > div > div._categoryButton_category_button_1lIOy > button').click()
        div = driver.find_element(By.CSS_SELECTOR, '#wrap > div._gnb_gnb_2C24o > div._gnb_header_area_150KE > div > div._gnbLogo_gnb_logo_3eIAf > div > div._categoryButton_category_button_1lIOy > div > div')
        list = div.find_element(By.CSS_SELECTOR, 'div._categoryLayer_main_category_2A7mb > ul')
        lis = list.find_elements(By.CLASS_NAME, '_categoryLayer_list_34UME')
        
        for li in lis:
            data = {}
            main = li.find_element(By.CSS_SELECTOR, 'a > span > img').get_attribute('alt')
            actions = webdriver.ActionChains(driver).move_to_element(li)
            actions.perform()
            midlist = driver.find_element(By.CSS_SELECTOR, '#wrap > div._gnb_gnb_2C24o > div._gnb_header_area_150KE > div > div._gnbLogo_gnb_logo_3eIAf > div > div._categoryButton_category_button_1lIOy > div > div > div._categoryLayer_middle_category_2g2zY > ul')
            midlis = midlist.find_elements(By.CLASS_NAME, '_categoryLayer_list_34UME')

            for midli in midlis:
                mid = midli.find_element(By.CSS_SELECTOR, 'a').text
                actions = webdriver.ActionChains(driver).move_to_element(midli)
                actions.perform()
                try:
                    sublist = driver.find_element(By.CSS_SELECTOR, '#wrap > div._gnb_gnb_2C24o > div._gnb_header_area_150KE > div > div._gnbLogo_gnb_logo_3eIAf > div > div._categoryButton_category_button_1lIOy > div > div > div._categoryLayer_subclass_1K649')
                    sublis = sublist.find_elements(By.CLASS_NAME, '_categoryLayer_list_34UME')
                    for subli in sublis:
                        sub = subli.find_element(By.CSS_SELECTOR, 'a').text
                        data = {'commerce_type':commerceType, 'main':main, 'mid':mid, 'sub':sub}
                        insert_data(self.dbconn, self.cursor, data)
                except NoSuchElementException:
                    sub = ''
                    data = {'commerce_type':commerceType, 'main':main, 'mid':mid, 'sub':sub}
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
GetTotalAds = GetData.total_category()

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