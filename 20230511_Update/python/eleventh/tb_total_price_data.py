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
            INSERT IGNORE INTO tb_total_price_data
            (
                PRODUCT_NAME, PRICE, STAR_SCORE, REVIEW_COUNT,  
                DELIVERY_PRICE, URL, 
                CREATED, UPDATED, UPDATER, COLLECTION_DATE, 
                COMMERCE_TYPE, ADS, CATEGORY
            ) 
            VALUES 
            (
                "{data['product_name']}", "{data['price']}",
                "{data['star_score']}", "{data['review_count']}",
                "{data['delivery_price']}", "{data['url']}", 
                "{data['created']}", "{data['updated']}", "{data['updater']}", "{data['collection_date']}", 
                "{data['commerce_type']}", "{data['ads']}", "{data['category']}"
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

    def total_event(self):
        url = 'https://www.11st.co.kr/products/pa/4243449533?inpu=&trTypeCd=22&trCtgrNo=895019'
        driver.get(url=url)
        time.sleep(5)

        info = driver.find_element(By.CLASS_NAME, 'l_product_side_info')

        productName = info.find_element(By.CLASS_NAME, 'title').text
        price = info.find_element(By.CLASS_NAME, 'value').text
        price = price.replace(',', '')
        price = (int)(price, base=0)
        delivery = info.find_element(By.XPATH, '//*[@id="layBodyWrap"]/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/dl/div[3]/dt/div/button/strong').text
        reviewCount = info.find_element(By.CSS_SELECTOR, '#layBodyWrap > div.l_content > div > div.l_product_cont_wrap > div > div.l_product_view_wrap > div.l_product_summary.l_product_summary_amazon > div.l_product_side_info > div.b_product_info_assist > div > a > strong').text
        starScore = info.find_element(By.CLASS_NAME, 'c_seller_grade').text
        category = driver.find_element(By.CLASS_NAME, 'c_product_category_path').find_element(By.CLASS_NAME, 'selected').text


        adsYn = 'Y'
        commerceType = 'ELEVEN_TH'
        created = datetime.now()
        updated = datetime.now()
        updater = 'root'
        collection_date = datetime.now()
        data = {
                'product_name':productName,
                'price':price,
                'star_score':starScore,
                'review_count':reviewCount,
                'delivery_price':delivery,
                'url':url,
                'created':created,
                'updated':updated,
                'updater':updater,
                'collection_date':collection_date,
                'commerce_type':commerceType,
                'ads':adsYn,
                'category':category
            }
        #print(productNo, productName, price, discountRate, totalPrice)
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
GetTotalAds = GetData.total_event()

conn.close()
driver.quit()
