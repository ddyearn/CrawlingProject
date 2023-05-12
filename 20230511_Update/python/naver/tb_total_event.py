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
            INSERT IGNORE INTO tb_total_event
            (
                PRODUCT_NO, PRODUCT_NAME, PRICE, DISCOUNT_RATE, 
                TOTAL_PRICE, PRODUCT_URL, URL
            ) 
            VALUES (
                "{data['product_no']}", "{data['product_name']}", "{data['price']}", "{data['discount_rate']}", 
                "{data['total_price']}", "{data['product_url']}", "{data['url']}"
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
        url = 'https://plusdeal.naver.com/?sort=1'
        driver.get(url=url)
        time.sleep(5)

        div = driver.find_element(By.CSS_SELECTOR, '#tab_container > div > div.listTab_plusdeal_product_area__5gLg_ > div > div')
        list = div.find_elements(By.CLASS_NAME, 'productCard_product_card_view__yt7Ji')
        for lis in list:
            productNo = lis.find_element(By.CSS_SELECTOR, 'div').get_attribute('id')
            productNo = re.sub(r'[^0-9]', '', productNo)
            if productNo == '':
                break
            productName = lis.find_element(By.XPATH, '//*[@id="title_' + str(productNo) + '"]').text
            trash = lis.find_element(By.XPATH, '//*[@id="title_' + str(productNo) + '"]/span').text
            productName = productName.replace(trash, '')
            productUrl = driver.find_element(By.CSS_SELECTOR, '#product_id_' + str(productNo) + ' > a').get_attribute('href')
            price = driver.find_element(By.CSS_SELECTOR, '#product_id_' + str(productNo) + ' > div.productCard_information__YEkjB > div.productCard_price_area__RleMi > div.productCard_price_wrap__WaX_2 > span.productCard_price__2waKK > span').text
            price = price.replace(',', '')
            price = (int)(price, base=0)
            discountRate = driver.find_element(By.CSS_SELECTOR, '#product_id_' + str(productNo) + ' > div.productCard_information__YEkjB > div.productCard_price_area__RleMi > div.productCard_price_wrap__WaX_2 > span.productCard_discount__tupNR').text
            discountRate = discountRate.replace('%', '').replace('할인율\n', '')
            discountRate = float(discountRate)
            try:
                totalPrice = driver.find_element(By.CSS_SELECTOR, '#product_id_' + str(productNo) + ' > div.productCard_information__YEkjB > div.productCard_price_area__RleMi > div.productCard_benefit__lQNjK > span').text
                totalPrice = totalPrice.replace(',', '')
                totalPrice = (int)(totalPrice, base=0)
            except NoSuchElementException:
                totalPrice = price
            data = {
                'product_no': productNo,
                'product_name':productName,
                'price':price,
                'discount_rate':discountRate,
                'total_price':totalPrice,
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
