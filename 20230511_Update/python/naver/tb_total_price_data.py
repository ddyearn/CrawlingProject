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
                PRODUCT_NAME, PRODUCT_NO, LIST_PRICE, PRICE, TOTAL_PRICE, STAR_SCORE, REVIEW_COUNT,  
                SALE_COMPANY, DELIVERY_PRICE, URL, DELIVERY_TYPE,
                BRAND_NAME, EVENT, 
                CREATED, UPDATED, UPDATER, COLLECTION_DATE, 
                COMMERCE_TYPE, ADS
            ) 
            VALUES 
            (
                "{data['product_name']}", "{data['product_no']}", "{data['list_price']}", "{data['price']}",
                "{data['total_price']}", "{data['star_score']}", "{data['review_count']}",
                "{data['sale_company']}", "{data['delivery_price']}", "{data['url']}", "{data['delivery_type']}", 
                "{data['brand_name']}", "{data['event']}", 
                "{data['created']}", "{data['updated']}", "{data['updater']}", "{data['collection_date']}", 
                "{data['commerce_type']}", "{data['ads']}"
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
        url = 'https://brand.naver.com/cheiljedang/products/6042668419?n_media=11068&n_rank=1&n_ad_'
        driver.get(url=url)
        time.sleep(5)

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

        adsYn = 'Y'
        commerceType = 'NAVER'
        created = datetime.now()
        updated = datetime.now()
        updater = 'root'
        collection_date = datetime.now()
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
                'url':url,
                'delivery_type':deliveryType,
                'brand_name':brandName,
                'event':event,
                'created':created,
                'updated':updated,
                'updater':updater,
                'collection_date':collection_date,
                'commerce_type':commerceType,
                'ads':adsYn
            }
        #print(productNo, productName, price, discountRate, totalPrice)
        insert_data(self.dbconn, self.cursor, data)



        
        '''
                'list_price': listPrice,
                'discount_price': discountPrice,

                'discount_rate_commerce':discountRateCommerce,
                'discount_coupon_name':discountCouponName,
                'discount_rate_double':discountRateDouble,
                'discount_coupon_name_double':discountCouponNameDouble,
                'best_rank':bestRank,

                'star_score':starScore,
                'star_score_best_rate':starScoreBestRate,
                'star_score_good_rate':starScoreGoodRate,
                'star_score_bad_rate':starScoreBadRate,
                'star_score_worst_rate':starScoreWorstRate,
                'review_count':reviewCount,

                'buy_count':buyCount,
                'sale_company':saleCompany,
                'delivery_price':deliveryPrice,
                'product_url':productUrl,
                'product_option':productOption,
                'delivery_type':deliveryType,
                'collect':collect,
                'brand_name':brandName,
                'category':category,
                'vendor_item_id':venderItemId,
                'event':event,
                'deal_project_name':dealProjectName,
                'deal_no':dealNo,
                'store_friend':storeFriend,
                'like_count':likeCount,
                'price_unit':priceUnit,
                'division':division,
                'created':created,
                'updated':updated,
                'updater':updater,
                'collection_date':collection_date,
                'commerce_type':commerceType,
                'discount_provider':discountProvider,
                'discount_price_commerce':discountPriceCommerce,
                'etc_delivery_name':etcDeliveryName,
                'search_word':searchWord,
                'ads_yn':adsYn,
                'url':url,
                'creator':creator
        
                data = {
                'product_no': productNo,
                'product_name':productName,
                'list_price': listPrice,
                'price':price,
                'discount_rate':discountRate,
                'discount_price': discountPrice,
                'discount_rate_commerce':discountRateCommerce,
                'discount_coupon_name':discountCouponName,
                'discount_double':discountDouble,
                'discount_rate_double':discountRateDouble,
                'discount_coupon_name_double':discountCouponNameDouble,
                'total_price':totalPrice,
                'best_rank':bestRank,
                'star_score':starScore,
                'star_score_best_rate':starScoreBestRate,
                'star_score_good_rate':starScoreGoodRate,
                'star_score_bad_rate':starScoreBadRate,
                'star_score_worst_rate':starScoreWorstRate,
                'review_count':reviewCount,
                'buy_count':buyCount,
                'sale_company':saleCompany,
                'delivery_price':deliveryPrice,
                'product_url':productUrl,
                'product_option':productOption,
                'delivery_type':deliveryType,
                'collect':collect,
                'brand_name':brandName,
                'category':category,
                'vendor_item_id':venderItemId,
                'event':event,
                'deal_project_name':dealProjectName,
                'deal_no':dealNo,
                'store_friend':storeFriend,
                'like_count':likeCount,
                'price_unit':priceUnit,
                'division':division,
                'created':created,
                'updated':updated,
                'updater':updater,
                'collection_date':collection_date,
                'commerce_type':commerceType,
                'discount_provider':discountProvider,
                'discount_price_commerce':discountPriceCommerce,
                'etc_delivery_name':etcDeliveryName,
                'search_word':searchWord,
                'ads_yn':adsYn,
                'url':url,
                'creator':creator
            }

            insert_data(self.dbconn, self.cursor, data)

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
            '''
            


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
GetTotalAds = GetData.total_event()

conn.close()
driver.quit()