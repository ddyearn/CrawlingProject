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
# 일반
# DB Insert
def insert_data(dbconn, cursor, data) : 
    try : 
        cursor.execute(f"""
            INSERT IGNORE INTO tb_total_event
            (
                PRODUCT_NO, PRODUCT_NAME, PRICE, PRODUCT_URL, URL
            ) 
            VALUES (
                "{data['product_no']}", "{data['product_name']}", "{data['price']}", "{data['product_url']}", "{data['url']}"
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
        url = 'https://search.shopping.naver.com/best/home?categoryCategoryId=ALL&categoryDemo=A00&categoryRootCategoryId=ALL&chartDemo=A00&chartRank=1&period=P1D&windowCategoryId=2&windowDemo=A00&windowRootCategoryId=20000060'
        driver.get(url=url)
        time.sleep(5)

        list = driver.find_elements(By.CLASS_NAME, 'imageProduct_item__KZB_F')
        for lis in list:
            productNo = lis.get_attribute('id')
            if productNo == '':
                break
            product = lis.find_element(By.CSS_SELECTOR, 'a')
            
            productName = product.find_element(By.CSS_SELECTOR, 'div.imageProduct_text_area__ik6VN > div.imageProduct_title__Wdeb1').text
            
            productUrl = product.get_attribute('href')
            price = product.find_element(By.CSS_SELECTOR, 'div.imageProduct_text_area__ik6VN > div.imageProduct_price__W6pU1 > strong').text
            price = price.replace(',', '')
            price = (int)(price, base=0)
            data = {
                'product_no': productNo,
                'product_name':productName,
                'price':price,
                'product_url':productUrl,
                'url':url
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
