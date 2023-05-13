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
        url = 'https://www.11st.co.kr/main'
        driver.get(url=url)
        time.sleep(5)

        commerceType = 'ELEVEN_TH'

        driver.find_element(By.CSS_SELECTOR, '#gnb > div > div.b_header_gnb > div > div.c_gnb_button_category > button').click()
        
        div = driver.find_element(By.XPATH, '//*[@id="gnbCategory"]/div/div[1]/div[2]/nav/ul')
        lis = div.find_elements(By.XPATH, 'li')
        
        for li in lis:
            data = {}
            main = li.find_element(By.XPATH, 'a').get_attribute('textContent')
            middiv = li.find_element(By.CSS_SELECTOR, 'div.box_2depth')
            grouplist = middiv.find_elements(By.CLASS_NAME, 'group')
            for midlist in grouplist:
                midlis = midlist.find_elements(By.XPATH, 'dd')
                for midli in midlis:
                    mid = midli.find_element(By.XPATH, 'a').get_attribute('textContent')
                    try:
                        subdiv = midli.find_element(By.CSS_SELECTOR, 'div.box_3depth')
                        sublis = subdiv.find_elements(By.XPATH, 'ul/li')
                        for subli in sublis:
                            sub = subli.find_element(By.XPATH, 'a').get_attribute('textContent')
                            print(main + " / " + mid + " / " + sub)
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
conn = pymysql.connect(host='127.0.0.1', port=3307, user='', password='', db='', charset='utf8')
cur = conn.cursor()

GetData = GetData(conn, cur)
GetTotalAds = GetData.total_category()

conn.close()
driver.quit()
