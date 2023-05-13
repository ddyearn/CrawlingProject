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
                PRODUCT_NAME,  PRICE, 
                DELIVERY_PRICE, PRODUCT_URL, 
                CREATED, UPDATED, UPDATER, COLLECTION_DATE, 
                COMMERCE_TYPE, SEARCH_WORD, ADS_YN
            ) 
            VALUES 
            (
                "{data['product_name']}", "{data['price']}",
                "{data['delivery_price']}", "{data['product_url']}", 
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
        url = 'https://search.11st.co.kr/Search.tmall?kwd=즉석밥'
        driver.get(url=url)
        time.sleep(5)

        sections = driver.find_elements(By.CSS_SELECTOR, '#layBodyWrap > div > div > div.l_search_content > div > section')
        for section in sections:
            try:
                ad = section.find_element(By.CLASS_NAME, 'help_ad')
            except NoSuchElementException:
                continue
            list = section.find_elements(By.CSS_SELECTOR, 'ul > li')
            for lis in list:
                productName = lis.find_element(By.CLASS_NAME, 'c_prd_name').text
                price = lis.find_element(By.CLASS_NAME, 'price').find_element(By.CLASS_NAME, 'value').text
                price = price.replace(',', '')
                price = (int)(price, base=0)

                deliveryPrice = lis.find_element(By.CLASS_NAME, 'delivery').text
                
                productUrl = lis.find_element(By.TAG_NAME, 'a').get_attribute('href')
                
                searchWord = '즉석밥'
                adsYn = 'Y'
                commerceType = 'ELEVEN_TH'
                created = datetime.now()
                updated = datetime.now()
                updater = 'root'
                collection_date = datetime.now()

                data = {
                    'product_name':productName,
                    'price':price,
                    'delivery_price':deliveryPrice,
                    'product_url':productUrl,
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
conn = pymysql.connect(host='127.0.0.1', port=3307, user='', password='', db='', charset='utf8')
cur = conn.cursor()

GetData = GetData(conn, cur)
GetTotalAds = GetData.total_ads()

conn.close()
driver.quit()

