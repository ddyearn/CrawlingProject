from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
import time

import pymysql
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import mysql.connector
from urllib.request import urlopen
from datetime import datetime
from pandas import DataFrame
import pyperclip
import subprocess
import re
# 일반
# DB Insert
def insert_data(dbconn, cursor, data) : 
    try : 
        cursor.execute(f"""
            INSERT IGNORE INTO tb_total_event
            (
                PRODUCT_NAME, PRICE, DELIVERY_PRICE, URL
            ) 
            VALUES (
                "{data['product_name']}", "{data['price']}", "{data['delivery_price']}", "{data['url']}"
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
        url = 'https://www.11st.co.kr/browsing/BestSeller.tmall?method=getBestSellerMain&xfrom=main^gnb#pageNum%%4'
        driver.get(url=url)
        time.sleep(5)

        lists = driver.find_elements(By.CLASS_NAME, 'ranking_pd')

        data={}
        for li in lists:
            item = li.find_element(By.TAG_NAME, 'p').text
            price = li.find_element(By.CLASS_NAME, 'sale_price').text
            price = price.replace(',', '')
            price = (int)(price, base=0)
            deliveryFee = li.find_element(By.CLASS_NAME, 's_flag').text
            url = li.find_element(By.TAG_NAME, 'a').get_attribute('href')

            data = {
                'product_name' : item, 
                'price' : price, 
                'delivery_price' : deliveryFee, 
                'url' : url
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
GetTotalAds = GetData.total_event()

conn.close()
driver.quit()
