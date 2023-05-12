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
            INSERT IGNORE INTO total_review
            ( PRODUCT_NAME, URL, COMMERCE_TYPE, CREATOR, STAR_SCORE, CONTENT ) 
            VALUES 
            ( "{data['product_name']}", "{data['url']}", "{data['commerce_type']}", "{data['creator']}", "{data['star_score']}", "{data['content']}" ) 
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

    def total_review(self):
        url = 'https://www.11st.co.kr/products/pa/4243449533?inpu=&trTypeCd=22&trCtgrNo=895019'
        driver.get(url=url)
        time.sleep(5)

        commerceType = 'ELEVEN_TH'
        
        data = {}

        productName = driver.find_element(By.CSS_SELECTOR, '#layBodyWrap > div.l_content > div > div.l_product_cont_wrap > div > div.l_product_view_wrap > div.l_product_summary.l_product_summary_amazon > div.l_product_side_info > div.c_product_info_title.appleshop_type > h1').text

        driver.find_element(By.ID, 'tabMenuDetail2').click()
        for c in range(0,10):
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
        reviews = driver.find_elements(By.CLASS_NAME, 'review_list_element')
        for review in reviews:
            print('???')
            cid = review.find_element(By.CLASS_NAME, 'c_product_reviewer').find_element(By.CLASS_NAME, 'name').text
            rstar = review.find_element(By.CLASS_NAME, 'grade').text
            content = review.find_element(By.CLASS_NAME, 'cont_review_hide').text
            print(cid+rstar+content[:10])
            data = {'product_name' : productName, 'url' : url, 'commerce_type' : commerceType, 'creator' : cid, 'star_rate' : rstar, 'content' : content}
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
GetTotalAds = GetData.total_review()

conn.close()
driver.quit()
